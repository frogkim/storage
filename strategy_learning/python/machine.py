# There are three neural networks in this machine.
# Network 1 predict actions.
# Network 2 predict actions when Network 1 predict wrongly.
# Network 3 predict with the data of Network1 and Network2.
# Numberinged Start buttons train each network. They are independently.

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import random, ctypes, time, os, tkinter, sys
from function import *

# TODO - prepocessing of data in train
# (DONE) TODO - reduce stop button as one -- need to fix in GUI class
# (DONE) TODO - create "initialize button"
# (DONE) TODO - fix start button it cannot be operated without initialization
# TODO - adjust neural as softmax and entropy cost

class MACHINE:
    def __init__(self, name="machine"):
        # setting for class
        self.switch = 0

        # tensorflow related setting
        self.session = tf.Session()

        # data format information
        # about urLinesAvg and urLinesInAnswer, refer to "dataloading(self)"
        self.tLines = 99840 # total lines of data
        self.urLinesInAvg = 144   # unreadable lines of avg data
        self.urLinesInAnswer = 11 # unreadable lines of ans data
        self.lines = self.tLines- self.urLinesInAvg - self.urLinesInAnswer
        self.currencies = 6
        self.avgs = 20
        self.ohlc = 4
        self.states = 3
        self.actions = 3

        # setting for neural net
        self.net_name = name
        self.l_rate = 1e-4
        self.minibatch = 1
        self.learning_sample_lines = 20 # learning sample lines
        self.neural_size = 128
        self.pred = []
        self.train = []
        self.x_input_size = self.currencies * self.avgs * self.learning_sample_lines
        
        # optimizer
        self.optimizer = tf.train.RMSPropOptimizer(learning_rate = self.l_rate)

        self.input_size = self.learning_sample_lines * self.currencies * self.avgs
        ## for RNN self.input_size = self.currencies * self.avgs
        self.output_size = self.states * self.actions# 3 states 3 actions

        # setting for train
        self.loss = 0        

        # create data sample and network
        self.dataloading()
        self._build_network()

        # setting for data -- must be operated after making network
        self.savemodel = './save/model'
        self.savefile = self.savemodel + '.index'
        self.saver = tf.train.Saver()

    # Settings
    def SetGUI(self, gui):
        self.gui = gui

    def SetAccuracy(self, value):
        self.gui.AccText.config(text=value)

    def SetLoss(self, value):
        self.gui.AccText2.config(text=value)

    def SetTotal(self, value):
        self.gui.AccText3.config(text=value)

    def SetTurn(self, value):
        self.gui.txTurn.config(text=value)

    def SetShort(self, value):
        self.gui.txShort.config(text=value)

    def SetNetr(self, value):
        self.gui.txEmpty.config(text=value)

    def SetLong(self, value):
        self.gui.txLong.config(text=value)

    # Buttons
    def turnon(self, value):
        self.switch = value
        if(value == 0): return "turned off"
        elif(value == 1): return "Type 1 machine is turned on"
        elif(value == 2): return "Type 2 machine is turned on"
        elif(value == 3): return "Type 3 machine is turned on"
        else: return "switch error"

    # data manage
    def normalize(self, ilist):
        vmax = np.max(ilist)
        vmin = np.min(ilist)
        return (ilist-vmin) / (vmax-vmin)
    
    def initialize(self):
        self.session.run(tf.global_variables_initializer())
        self.gui.initialize = True

    def restore(self):
        if(os.path.isfile(self.savefile)):
            self.saver.restore(self.session, self.savemodel)
            self.gui.initialize = True
            message = "retore success"
        else:
            message = "no model file"
        return message

    def save(self):
        save_path = ""
        save_path = self.saver.save(self.session, self.savemodel)
        if not (save_path == ""):
            message = "save success"
        else:
            message = "save failed"
        return message

    def dataloading(self):
        # change shape of data
        self.x_price = []
        for i in range(6): self.x_price.append(SetupPrice(i))
        self.x_price = np.array(self.x_price)
        self.x_price = self.x_price[:, self.urLinesInAnswer:self.tLines-self.urLinesInAvg, :]
        
        # In avg.dat, 99840-144 lines are stored. It starts index from 144 to 99840
        # stored data's element size is 64 bits(float64). It should be changed to float32
        # Abandon last 11 lines to fit with y answer
        
        self.x_avg = SetupAVG()
        self.x_avg = self.x_avg.reshape([self.tLines-self.urLinesInAvg, self.avgs*self.currencies])
        self.x_avg = self.x_avg[:self.lines, :]
        self.x_avg = self.x_avg.astype(np.float32) 

        # make hot-key
        # In ans*.dat, last 11 lines are not stored. It index is from 0 to 99840 - 11
        # It will be fixed in Q-learning
        self.y_ans = np.zeros([self.currencies, self.tLines, self.states, self.actions])
        self.y_ans = self.y_ans.astype(np.float32)
        y_array = []    # temporary list to make minibatch
        for i in range(6): y_array.append(SetupANS(i))
        y_array = np.array(y_array)
        y_array = y_array[:, self.urLinesInAvg:, :]
        for i in range(self.currencies):
            for j in range(self.lines):
                for k in range(3):
                    if(y_array[i,j,k] == 0):    self.y_ans[i,j,k,0] = 1.0
                    elif(y_array[i,j,k] == 1):  self.y_ans[i,j,k,1] = 1.0
                    else:                       self.y_ans[i,j,k,2] = 1.0

    def _build_network(self):
        layerlist = []

        # placeholder X and Y
        self.X = tf.placeholder(tf.float32, [None, self.input_size], name="input_x")
        self.Y = []
        for i in range(3): 
            self.Y.append(tf.placeholder(shape=[None, self.states], dtype=tf.float32))

        for i in range(3): 
            layer, train = self.neurals_1(i)
            layerlist.append(layer)
            self.train.append(train)

        self.pred, self.trainloss, train = self.neurals_2(layerlist)
        self.train.append(train)


    def neurals_1(self, name):
        self.net_name += "_" + str(name)
        weights = []
        with tf.variable_scope(self.net_name):
            # Test #1
            # weights
            weight_name = self.net_name + "_1"
            weights.append(tf.get_variable(weight_name, shape=[self.input_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_2"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_3"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_4"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_5"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            
            # Q prediction
            layer1 = tf.nn.tanh(tf.matmul(self.X, weights[0]))
            layer2 = tf.nn.tanh(tf.matmul(layer1, weights[1]))
            ### useless delete
            loss = 0
            pred1 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer2, weights[2])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[0], logits = pred1)
            pred2 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer2, weights[3])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[1], logits = pred2)
            pred3 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer2, weights[4])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[2], logits = pred3)
            
            # Loss function
            loss = tf.reduce_mean(loss)
            grads_and_vars = self.optimizer.compute_gradients(loss, weights)
            train = self.optimizer.apply_gradients(grads_and_vars)
            return layer2, train
            

    def neurals_2(self, layerlist):
        self.net_name += "_aggregate"
        weights = []
        with tf.variable_scope(self.net_name):
            # weights
            weight_name = self.net_name + "_1"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_2"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_3"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_4"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_5"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            weight_name = self.net_name + "_6"
            weights.append(tf.get_variable(weight_name, shape=[self.neural_size, self.actions],
                                 initializer = tf.keras.initializers.glorot_uniform()))
            
            # Q prediction
            layer1 = tf.nn.tanh(tf.matmul(layerlist[0], weights[0]))
            layer2 = tf.nn.tanh(tf.matmul(layerlist[1], weights[1]))
            layer3 = tf.nn.tanh(tf.matmul(layerlist[2], weights[2]))
            layer = layer1 + layer2 + layer3
            loss = 0
            pred1 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer, weights[3])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[0], logits = pred1)

            pred2 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer, weights[4])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[1], logits = pred2)

            pred3 = tf.nn.softmax(tf.nn.tanh(tf.matmul(layer, weights[5])))
            loss += tf.nn.softmax_cross_entropy_with_logits(labels = self.Y[2], logits = pred3)
            
            # Loss function
            loss = tf.reduce_mean(loss)
            grads_and_vars = self.optimizer.compute_gradients(loss, weights)
            train = self.optimizer.apply_gradients(grads_and_vars)
            return [pred1, pred2, pred3], loss, train

    def reset(self, turn=0):
        self.result = [0,0,0]
        self.count = 0
        self.correct = 0
        self.turn = turn
        self.loss = 0

    def updateGUI(self):
        self.SetShort(self.result[0])
        self.SetNetr(self.result[1])
        self.SetLong(self.result[2])
        if self.count > 0:
            self.SetAccuracy(self.correct / self.count)
            self.SetLoss(self.loss * 3 / self.count)
        self.SetTotal(self.count)
        self.SetTurn(self.turn)

    def SetScore(self, pred):
        pred = np.array(pred)
        pred = pred.reshape([self.minibatch, self.states, self.actions])
        score = 0
        # score pass rate
        for i in range(self.minibatch):
            for j in range(self.states):
                if( np.argmax(pred[i][j]) == np.argmax(self.y_stack[i][j]) ):
                    score += 1
                if( np.argmax(pred[i][j]) == 0):     self.result[0] += 1
                elif( np.argmax(pred[i][j]) == 1):   self.result[1] += 1
                else:                                self.result[2] += 1
        return score, score / (self.minibatch*self.states)

    # main function
    def operate(self):
        self.reset()
        balance = 0
        while(1):
            if self.gui.exit is True: break
            if(self.switch == 0): continue

            if(self.count > 3*10000): #test 30000 lines and reset
                self.turn += 1
                self.reset(self.turn)
            
            x_list = []
            y_list = []

            # stack data list
            for i in range(self.minibatch):
                index = random.randrange(self.learning_sample_lines, self.lines)
                #x_list.append(self.normalize(self.x_avg[index:index+self.learning_sample_lines, :]))
                x_input = self.x_avg[index-self.learning_sample_lines+1:index+1, :]
                x_input = x_input.reshape([self.x_input_size])
                x_list.append(x_input)
                y_list.append(self.y_ans[0, index])

            # organize for machine method    
            self.x_stack = np.array(x_list)
            self.y_stack = np.array(y_list)
            
            # predict - to avoid kink, use balance variable
            if(self.y_stack[0,0,2] == 1):    
                if not (balance % 3 == 0): continue
            elif(self.y_stack[0,2,0] == 1):  
                if not (balance % 3 == 1): continue
            else:
                if not (balance % 3 == 2): continue

            pred = self.predict()
            _, _ = self.update(balance%3)
            balance += 1
            score, passrate = self.SetScore(pred)
            loss, _ = self.update(3)
            self.correct += score
            self.loss += loss
            self.count += self.states * self.minibatch
            # update GUI
            self.updateGUI()

            # empty list for next train
            x_list.clear()
            y_list.clear()
            continue # return to while

    # build network    # predict
    def predict(self):
        return self.session.run(self.pred, feed_dict={self.X: self.x_stack})

    # learning
    def update(self, index):
        #dict = {}
        #for i in range(3): dict['_Y[' + i + ']'] = 'y_stack[' + i + ']'
        return self.session.run([self.trainloss, self.train[index]], feed_dict={
                                    self.X: self.x_stack,
                                    self.Y[0]: self.y_stack[:,0],
                                    self.Y[1]: self.y_stack[:,1], 
                                    self.Y[2]: self.y_stack[:,2]})
