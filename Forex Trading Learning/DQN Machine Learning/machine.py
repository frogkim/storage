import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
import numpy as np
import random, os
from collections import deque
from neurals import NUERALS
from trading import TRADING


class MACHINE:
    def __init__(self, name="machine"):
        # setting for class
        self.switch = 0
        self.count = 0
        self.initialize = False

        # tensorflow related setting
        self.session = tf.Session()
        self.mainDQN = NUERALS(self.session, "main")
        self.targetDQN = NUERALS(self.session, "target")

        # setting for data -- must be operated after making network
        self.savemodel = './save/model'
        self.savefile = self.savemodel + '.index'
        self.saver = tf.train.Saver()

        # create data sample and network
        self.x_price, self.x_avg = self._dataloading()
        self.trading = TRADING(self.x_price, self.x_avg)

    # Settings
    def SetGUI(self, gui):
        self.gui = gui
        self.trading.SetGUI(gui)

    # update GUI
    def UpdateGUI(self):
        self.trading.UpdateGUI()

    # reset
    def Reset(self):
        self.count = 0

    # Buttons
    def TurnOn(self, value):
        self.switch = value
        if (value == 0):
            return "turned off"
        elif (value == 1):
            return "Machine is turned on"
        else:
            return "switch error"

    def TurnOff(self):
        self.mainDQN.GraphClose()

    def SetSwitch(self, value):
        self.switch = value

    # Initializie
    def Initialize(self):
        self.session.run(tf.global_variables_initializer())
        self.initialize = True

    def GetInitialize(self):
        return self.initialize

    def Restore(self):
        if os.path.isfile(self.savefile):
            self.saver.restore(self.session, self.savemodel)
            self.initialize = True
            message = "restore success"
        else:
            message = "no model file"
        return message

    def Save(self):
        save_path = ""
        save_path = self.saver.save(self.session, self.savemodel)
        if not (save_path == ""):
            message = "save success"
        else:
            message = "save failed"
        return message

    # data manage
    def _normalize(self, ilist):
        vmax = np.max(ilist)
        vmin = np.min(ilist)
        return (ilist - vmin) / (vmax - vmin)

    def _dataloading(self):
        # change shape of data
        x_price = [self._setupPrice(i) for i in range(6)]
        x_price = np.array(x_price)
        x_price = x_price[:, 144:99840, :]
        x_avg = self._setupAVG()  # SetupAVG : [144 : 99840, cols]
        return np.array(x_price), x_avg

    def _fileString(self, cur_num):

        if cur_num == 0: return "eurusd"
        if cur_num == 1: return "gbpusd"
        if cur_num == 2: return "audusd"
        if cur_num == 3: return "usdchf"
        if cur_num == 4: return "usdcad"
        if cur_num == 5: return "usdjpy"

    def _setupPrice(self, cur_num):
        rows = 99840
        cols = 4
        filename = "../data/" + self._fileString(cur_num) + ".dat"
        f = open(filename, "rb")
        price = np.fromfile(f, dtype=np.float64, count=-1, sep="", offset=0)
        price = price.reshape([rows, cols])
        f.close()
        return price

    def _setupAVG(self):
        rows = 99840 - 144
        cols = 20 * 6
        filename = "../data/" + "avg.dat"
        f = open(filename, "rb")
        avg = np.fromfile(f, dtype=np.float64, count=-1, sep="", offset=0)
        avg = avg.reshape([rows, cols])
        f.close()
        return avg

    # main function
    def Operate(self):
        startIndex = 1
        totalIndex = 99840 - 144
        minibatch = 10
        avgs = 120
        learning_sample_lines = 20  # learning sample lines
        oneGameTime = 100

        epsilon = 0.2
        gamma = 0.99
        state = 1
        step = 0

        while self.switch > -1:
            if self.switch == 0:
                continue
            q_stack = np.zeros([oneGameTime, 3])
            actions = np.ones(oneGameTime)
            self.count += 1
            index = random.randrange(startIndex + learning_sample_lines, totalIndex - oneGameTime - 1)
            x_sample = self.x_avg[index - learning_sample_lines + 1: index + oneGameTime + 1, :]
            for i in range(oneGameTime):
                if self.switch == 0: break
                if random.random() < epsilon:
                    action = random.randrange(0, 3, 1)
                else:
                    x_stack = x_sample[i:i + learning_sample_lines, :]
                    x_stack = x_stack.reshape([1, learning_sample_lines, avgs])
                    x_stack = self._normalize(x_stack)
                    prediction = self.targetDQN.Predict(x_stack)
                    action = np.argmax(prediction[0, 0])
                reward = self.trading.Play(i, state, action)
                # In this game, the player cannot affect to environment
                # It is not used to store state
                q_stack[i, action] = reward
                actions[i] = action
                state = action
            self.trading.Close(index + oneGameTime, state)

            for i in range(oneGameTime - 2, -1):
                reward_next = np.max(q_stack[i + 1])
                q_stack[i, actions[i]] += gamma * reward_next

            x_stack = []
            y_stack = []
            for i in range(minibatch):
                index = random.randint(0, oneGameTime - 1)
                x_stack.append(self._normalize(x_sample[index:index + learning_sample_lines, :]))
                y_stack.append(q_stack[index])
            x_stack = np.array(x_stack)
            x_stack = x_stack.reshape([minibatch, learning_sample_lines, avgs])
            y_stack = np.array(y_stack)
            y_stack = y_stack.reshape([minibatch, 1, 3])
            _, _, graph = self.mainDQN.Update(x_stack, y_stack)
            step += 1

            self.gui.SetTotal(self.count)

            if self.count == 200:
                self.targetDQN.Copy(self.mainDQN)
                self.mainDQN.StoreGraph(graph, step)
                self.Reset()
                self.trading.Reset(step)
                self.Save()

