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
        self.mainDQN.GraphClose()
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
        """
            Mnih, V., Kavukcuoglu, K., Silver, D. et al.
            Human-level control through deep reinforcement learning. Nature 518, 529–533 (2015).
            https://doi.org/10.1038/nature14236
            
            Algorithm 1: deep Q-learning with experience replay
            Initialize replay memory D to capacity N
            Initialize action-value function  with random weights θ
            Initialize target action-value function  with weights θ^− = θ
            
            For episode = 1, M do
                Initialize sequence s_1 = {x_1} and preprocessed sequence Φ_1 = Φ(s_1)
                For t = 1,T do
                    With probability ε select a random action a_t
                    otherwise select a_t = argmax_a Q(Φ(s_t), a; theta)
                    Execute action at in emulator and observe reward rt and image x_t+1
                    Set s_t+1 = s_t, a_t, x_t+1 and preprocess 
                    Store transition (Φ_t, a_t, r_t, Φ_t+1) in D
                    Sample random minibatch of transitions(Φ_t, a_t, r_t, Φ_t+1) from D
                    Set 
                        y_j = r_j 						if episode termnmiates ate step j+1
                    or	y_j = r_j + gamma * max_d Q^ (Φ_j+1, a'; θ^−)		otherwise
            
                    Perform a gradient descent step on (y_j - Q(Φ_j, a_j ; θ) )^2
                    with respect to the network parameters θ
                    Every C steps reset Q^ = Q
                End For
            End For            
            """
        startIndex = 1
        totalIndex = 99840 - 144
        minibatch = 10
        avgs = 120
        learning_sample_lines = 20  # learning sample lines
        oneGameTime = 100

        epsilon = 0.2
        gamma = 0.99
        reward = 0
        action = 1
        state = 1

        while (1):
            if self.switch == 0:
                continue
            q_stack = np.zeros([oneGameTime, 3])
            actions = np.ones(oneGameTime)
            self.count += 1
            index = random.randrange(startIndex + learning_sample_lines, totalIndex - oneGameTime)
            x_sample = self.x_avg[index - learning_sample_lines + 1: index + oneGameTime + 1, :]
            for i in range(oneGameTime):
                if self.switch == 0:
                    self.Reset()
                    self.trading.Reset()
                    break
                if random.random() < epsilon:
                    action = random.randrange(0, 3, 1)
                else:
                    x_stack = x_sample[i:i+learning_sample_lines, :]
                    x_stack = x_stack.reshape([1, learning_sample_lines, avgs])
                    x_stack = self._normalize(x_stack)
                    prediction = self.targetDQN.Predict(x_stack)
                    action = np.argmax(prediction[0,0])
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
                if self.switch == 0:
                    self.Reset()
                    self.trading.Reset()
                    break
                index = random.randint(0, oneGameTime-1)
                x_stack.append(x_sample[index:index + learning_sample_lines, :])
                y_stack.append(q_stack[index])
            x_stack = np.array(x_stack)
            x_stack = x_stack.reshape([minibatch, learning_sample_lines, avgs])
            y_stack = np.array(y_stack)
            y_stack = y_stack.reshape([minibatch, 1, 3])
            _, _, graph = self.mainDQN.Update(x_stack, y_stack)

            self.gui.SetTotal(self.count)

            if self.count % 5 == 4:
                self.targetDQN.Copy(self.mainDQN)

            if self.count == 1000:
                self.mainDQN.StoreGraph(graph, self.count)

                self.Reset()
                self.trading.Reset()
                self.Save()


