import numpy as np


class TRADING:
    def __init__(self, x_price, x_avg):
        self.x_price = x_price
        self.x_avg = x_avg
        self.startIndex = 0
        self.totalIndex = 99840 - 144

        self.openPrice = 0
        self.balance = 1000
        self.maxBalance = 1000
        self.minBalance = 1000
        self.drawDown = 0

        self.long = 0
        self.long_win = 0
        self.long_loss = 0
        self.long_rate = 0

        self.short = 0
        self.short_win = 0
        self.short_loss = 0
        self.short_rate = 0

        #self.step = 1e-5 * 1
        self.fee = 1e-5 * 30

    def SetGUI(self, gui):
        self.gui = gui

    def UpdateGUI(self):
        self.long = self.long_win + self.long_loss
        self.short = self.short_win + self.short_loss

        self.gui.SetBalance("{:0.4f}".format(self.balance))
        self.gui.SetDrawDown("{:0.4f}".format(self.drawDown))
        self.gui.SetLong(self.long)
        self.gui.SetLongWin(self.long_win)
        self.gui.SetLongLoss(self.long_loss)

        self.gui.SetShort(self.short)
        self.gui.SetShortWin(self.short_win)
        self.gui.SetShortLoss(self.short_loss)

        if self.long > 0: self.gui.SetLongRate(("{:0.4f}".format(self.long_win / self.long)))
        if self.short > 0: self.gui.SetShortRate(("{:0.4f}".format(self.short_win / self.short)))

    def GetBalance(self):
        return self.balance

    def SetOpenPrice(self, index):
        self.openPrice = self.x_price[0, index, 0]

    def Reset(self, step):
        if self.long != 0 and self.short != 0:
            message = "Step : " + str(step)
            message += ", Balance : {:0.4f}".format(self.balance)
            message += ", DrawDown : {:0.2f} %".format(self.drawDown*100)
            message += ", Long : {0}".format(self.long)
            message += ", Short : {0}".format(self.short)
            message += ", LongRatio : {:0.4f}".format(self.long_win / self.long)
            message += ", ShortRatio : {:0.4f}".format(self.short_win / self.short)
            print(message)
            f = open("result.txt", "a")
            f.write(message)
            f.write("\n")
            f.close()

        self.openPrice = 0
        self.balance = 1000
        self.maxBalance = 1000
        self.minBalance = 1000
        self.drawDown = 0


        self.long = 0
        self.long_win = 0
        self.long_loss = 0
        self.long_rate = 0

        self.short = 0
        self.short_win = 0
        self.short_loss = 0
        self.short_rate = 0

    def Play(self, index, state, action):
        result = 0
        if self.openPrice != 0: profit = self.x_price[0, index, 0] - self.openPrice

        if state == 0:
            if action != 0:
                self.openPrice = 0
                result -= self.fee
                result -= profit
                if result > 0:
                    self.short_win += 1
                else:
                    self.short_loss += 1

                if action == 2:
                    self.openPrice = self.x_price[0, index, 0]
                    result -= self.fee

        elif state == 1:
            if action != 1:
                self.openPrice = self.x_price[0, index, 0]
                result -= self.fee
                if action == 0:
                    self.short += 1
                else:
                    self.long += 1

        else:
            if action != 2:
                self.openPrice = 0
                result -= self.fee
                result += profit
                if result > 0:
                    self.long_win += 1
                else:
                    self.long_loss += 1

                if action == 0:
                    self.openPrice = self.x_price[0, index, 0]
                    result -= self.fee

        self.balance += result
        if self.maxBalance < self.balance: self.maxBalance = self.balance
        if self.minBalance > self.balance: self.minBalance = self.balance
        self.drawDown = (self.maxBalance - self.minBalance) / self.maxBalance
        self.UpdateGUI()
        return result
