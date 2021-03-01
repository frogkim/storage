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
        self.trigger = [False, False, False]

        # tensorflow related setting
        self.session = tf.Session()

        # setting for neural net
        self.net_name = name
             #### self.minibatch = 10
        self.tLines = 99840 # total lines of data
        self.urLines = 11 # unreadable lines of data
        self.currencies = 6
        self.avgs = 20
        self.learning_sample_lines = 20 # learning sample lines

        self.states = 3
        self.actions = 3
        
        self.neural_size = 128
        
        self.input_size = self.currencies * self.avgs * self.learning_sample_lines
        self.output_size = self.actions# 3 states 3 actions

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
    def turn_one(self, trigger):
        if(trigger is True):
            if(self.trigger[1] is True):
                message = "Turn off type 2 machine"
                return message
            if(self.trigger[2] is True):
                message = "Turn off type 3 machine"
                return message
        
        self.trigger[0] = trigger
        if(self.trigger[0]):
            message = "Type 1 machine is turned on"
        else:
            message = "Type 1 machine is turned off"
        return message

    def turn_two(self, trigger):
        if(trigger is True):
            if(self.trigger[0] is True):
                message = "Turn off type 1 machine"
                return message
            if(self.trigger[2] is True):
                message = "Turn off type 3 machine"
                return message

        self.trigger[1] = trigger
        if(self.trigger[1]):
            message = "Type 2 machine is turned on"
        else:
            message = "Type 2 machine is turned off"
        return message

    def turn_three(self, trigger):
        if(trigger is True):
            if(self.trigger[0] is True):
                message = "Turn off type 1 machine"
                return message
            if(self.trigger[1] is True):
                message = "Turn off type 2 machine"
                return message

        self.trigger[2] = trigger
        if(self.trigger[2]):
            message = "Type 3 machine is turned on"
        else:
            message = "Type 3 machine is turned off"
        return message

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
        self.x_price = []
        self.x_avg = []
        self.y_ans = np.zeros([6, 99840-11, 9])
        self.y_ans = self.y_ans.astype(np.float32)

        y_array = []    # temporary list to make minibatch
        for i in range(6):
            self.x_price.append(SetupPrice(i))
            self.x_avg.append(SetupAVG(i))
            y_array.append(SetupANS(i))
            
        # change shape of data
        self.x_price = np.array(self.x_price)
        self.x_price = self.x_price.reshape([6, 99840, 4])
        
        self.x_avg = np.array(self.x_avg)
        self.x_avg = self.x_avg.reshape([6, 99840, 20])
        self.x_avg = self.x_avg.astype(np.float32) # change data type double -> float

        # make hot-key
        y_array = np.array(y_array)
        y_array = y_array.reshape([6, 99840-11, 3])
        for i in range(6):
            for j in range(99840-11):
                for k in range(3):
                    if(y_array[i,j,k] == 0):
                        self.y_ans[i,j,3*k  ] = 1.0
                        self.y_ans[i,j,3*k+1] = 0.0
                        self.y_ans[i,j,3*k+2] = 0.0
                    elif(y_array[i,j,k] == 1):
                        self.y_ans[i,j,3*k  ] = 0.0
                        self.y_ans[i,j,3*k+1] = 1.0
                        self.y_ans[i,j,3*k+2] = 0.0
                        
                    else:
                        self.y_ans[i,j,3*k  ] = 0.0
                        self.y_ans[i,j,3*k+1] = 0.0
                        self.y_ans[i,j,3*k+2] = 1.0

    def _build_network(self, lines=20):
        with tf.variable_scope(self.net_name):
            curs  = 6  # number of currency
            lines = 20 # read lines
            avgs  = 20 # avrage lines data from C
            # input_size = 20 * 6 * lines
            self.input_size = curs*lines*avgs
            self.output_size = 9 # 3 states * 3 actions
            self.l_rate=1e-4
            
            # optimizer
            self.optimizer = tf.train.RMSPropOptimizer(learning_rate = self.l_rate)

            # placeholder X and Y
            self._X = tf.placeholder(
                tf.float32, [None, self.input_size], name="input_x")
            
            self._Y = tf.placeholder(
                shape=[None, self.output_size], dtype=tf.float32)

            # Test #1
            # weights
            self.name = "test1_neural_"
            self.weight_name = self.name + "1"
            test1_weight_1 = tf.get_variable(self.weight_name, shape=[self.input_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "2"
            test1_weight_2 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "3_1"
            test1_weight_3_1 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.output_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "3_2"
            test1_weight_3_2 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.output_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "3_3"
            test1_weight_3_3 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.output_size],
                                 initializer = tf.keras.initializers.glorot_uniform())

            
            # Q prediction
            self.test1_layer1 = tf.nn.tanh(tf.matmul(self._X,           test1_weight_1))
            self.test1_layer2 = tf.nn.tanh(tf.matmul(self.test1_layer1, test1_weight_2))
            self.Qpred_1_1    = tf.nn.tanh(tf.matmul(self.test1_layer2, test1_weight_3_1))
            self.Qpred_1_2    = tf.nn.tanh(tf.matmul(self.test1_layer2, test1_weight_3_2))
            self.Qpred_1_3    = tf.nn.tanh(tf.matmul(self.test1_layer2, test1_weight_3_3))
            self.Qpred_1 = tf.reshape(self.Qpred_1, [self.states,self.actions])
            self.Qpred_1 = tf.reshape([tf.nn.softmax(self.Qpred_1[0,0:3]),
                                       tf.nn.softmax(self.Qpred_1[1,3:6]),
                                       tf.nn.softmax(self.Qpred_1[2,6:9])],
                                       [self.states,self.actions])
            
            

            # Loss function
            self.loss_1 = tf.reduce_mean(tf.square(self._Y - self.Qpred_1))
            self.train_1 = self.optimizer.minimize(self.loss_1)
            
            # Test #2
            # weights
            self.name = "test2_neural_"
            self.weight_name = self.name + "1"
            test2_weight_1 = tf.get_variable(self.weight_name, shape=[self.input_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "2"
            test2_weight_2 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            self.weight_name = self.name + "3"
            test2_weight_3 = tf.get_variable(self.weight_name, shape=[self.neural_size, self.output_size],
                                 initializer = tf.keras.initializers.glorot_uniform())
            
            # Q prediction
            self.test2_layer1 = tf.nn.tanh(tf.matmul(self._X,           test2_weight_1))
            self.test2_layer2 = tf.nn.tanh(tf.matmul(self.test2_layer1, test2_weight_2))
            self.Qpred_2      = tf.nn.tanh(tf.matmul(self.test2_layer2, test2_weight_3))

            # Loss function
            self.loss_2 = tf.reduce_mean(tf.square(self._Y - self.Qpred_2))
            self.train_2 = self.optimizer.minimize(self.loss_2)

            # Test #3
            # weights
            wlist = []
            self.name = "test3_neural_"

            self.weight_name = self.name + "1"
            wlist.append(tf.get_variable(self.weight_name, shape=[self.input_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))

            self.weight_name = self.name + "2"
            wlist.append(tf.get_variable(self.weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))

            self.weight_name = self.name + "3"
            wlist.append(tf.get_variable(self.weight_name, shape=[self.neural_size, self.neural_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))

            self.weight_name = self.name + "4"
            wlist.append(tf.get_variable(self.weight_name, shape=[self.neural_size, self.output_size],
                                 initializer = tf.keras.initializers.glorot_uniform()))

            # Q prediction
            self.test3_layer1 = tf.nn.tanh(tf.matmul(self._X,           wlist[0]))

            self.test3_layer2 = self.test1_layer2 * self.test3_layer1
            self.test3_layer2 = tf.nn.relu(tf.matmul(self.test3_layer2, wlist[1]))

            self.test3_layer3 = self.test2_layer2 * self.test3_layer1
            self.test3_layer3 = tf.nn.relu(tf.matmul(self.test3_layer2, wlist[2]))

            self.test3_layer4 = self.test3_layer2 + self.test3_layer3
            self.Qpred_3      = tf.nn.tanh(tf.matmul(self.test3_layer3, wlist[3]))

            # Loss function
            self.loss_3 = tf.reduce_mean(tf.square(self._Y - self.Qpred_3))
            self.grads_and_vars = self.optimizer.compute_gradients(self.loss_3, wlist)
            self.train_3 = self.optimizer.apply_gradients(self.grads_and_vars)

    def reset(self, turn=0):
        self.result = [0,0,0]
        self.count = 0
        self.correct = 0
        self.turn = turn

    def updateGUI(self):
        self.SetShort(self.result[0])
        self.SetNetr(self.result[1])
        self.SetLong(self.result[2])
        if self.count > 0:
            self.SetAccuracy(self.correct / self.count)
            self.SetLoss(self.loss * 3 / self.count)
        self.SetTotal(self.count)
        self.SetTurn(self.turn)

    # main function
    def operate(self):
        self.reset()
        while(1):
            if self.gui.exit is True: break

            if(self.count > 3*10000): #test 30000 lines and reset
                self.turn += 1
                self.reset(self.turn)
            
            if (self.trigger[0] is True or self.trigger[1] is True or self.trigger[2] is True):
                worklist = []
                x_list = []
                y_list = []

                self.count += self.states
                score = 0

                # stack data list
                index = random.randrange(self.learning_sample_lines, self.tLines - self.urLines)
                for j in range(self.learning_sample_lines):
                    x_list.append(self.x_avg[:, index + j-self.learning_sample_lines+1, :])
                # <A statement for using mini batch> y_list.append(self.y_ans[0, index, :]

                # organize for machine method    
                x_stack = np.array(x_list)
                x_stack = x_stack.reshape([1,self.input_size])
                x_stack = self.normalize(x_stack)
                # <A statement for using mini batch> y_stack = np.array(y_list)
                y_stack = np.array(self.y_ans[0, index, :])
                y_stack = y_stack.reshape([1,self.output_size])

                if(self.trigger[2] is False):
                    # predict
                    pred = self.predict_1(x_stack)

                    # analyse result
                    y_pred = np.array(pred)
                    y_pred = y_pred.reshape([self.states, self.actions])
                    y_answ = np.array(y_stack)
                    y_answ = y_answ.reshape([self.states, self.actions])

                    # score pass rate
                    for i in range(self.states):
                        if( np.argmax(y_pred[i]) == np.argmax(y_answ[i]) ):
                            score += 1

                    # neural 1 train
                    if(self.trigger[0] is True):
                        for i in range(self.states):
                            if( np.argmax(y_pred[i]) == np.argmax(y_answ[i]) ):
                                self.correct +=1

                        loss, _ = self.update_1(x_stack, y_stack)
                        self.loss += loss

                    # neural 2 train
                    if(self.trigger[1] is True):
                        # when neural 1 predict wrongly
                        if(score < 3):
                            # predict again by neural 2
                            pred = self.predict_2(x_stack)

                            # analyse result
                            y_pred = np.array(pred)
                            y_pred = y_pred.reshape([self.states, self.actions])
                            y_answ = np.array(y_stack)
                            y_answ = y_answ.reshape([self.states, self.actions])

                            for i in range(self.states):
                                if( np.argmax(y_pred[i]) == np.argmax(y_answ[i]) ):
                                    self.correct +=1

                            # train
                            loss, _ = self.update_2(x_stack, y_stack)
                            self.loss += loss

                else: # train 3
                        # predict again by neural 2
                        pred = self.predict_3(x_stack)
                        # analyse result
                        y_pred = np.array(pred)
                        y_pred = y_pred.reshape([self.states, self.actions])
                        y_answ = np.array(y_stack)
                        y_answ = y_answ.reshape([self.states, self.actions])
                        for i in range(self.states):
                            if( np.argmax(y_pred[i]) == np.argmax(y_answ[i]) ):
                                self.correct +=1

                        # train
                        loss, _ = self.update_3(x_stack, y_stack)
                        self.loss += loss
                # <TEMPORARY> machine's result.
                for i in range(self.states):
                    if( np.argmax(y_pred[i]) == 0):     self.result[0] += 1
                    elif( np.argmax(y_pred[i]) == 1):   self.result[1] += 1
                    else:                               self.result[2] += 1
                
                # update GUI
                self.updateGUI()

                # empty list for next train
                x_list.clear()
                y_list.clear()
                continue # return to while

    # build network    # predict
    def predict_1(self, state):
        x = np.reshape(state, [1, self.input_size])
        return self.session.run(self.Qpred_1, feed_dict={self._X: x})

    def predict_2(self, state):
        x = np.reshape(state, [1, self.input_size])
        return self.session.run(self.Qpred_2, feed_dict={self._X: x})

    def predict_3(self, state):
        x = np.reshape(state, [1, self.input_size])
        return self.session.run(self.Qpred_3, feed_dict={self._X: x})

    # learning
    def update_1(self, x_stack, y_stack):
        return self.session.run([self.loss_1, self.train_1], feed_dict={
                                    self._X: x_stack, self._Y: y_stack})

    def update_2(self, x_stack, y_stack):
        return self.session.run([self.loss_2, self.train_2], feed_dict={
                                    self._X: x_stack, self._Y: y_stack})

    def update_3(self, x_stack, y_stack):
        return self.session.run([self.loss_3, self.train_3], feed_dict={
                                    self._X: x_stack, self._Y: y_stack})
