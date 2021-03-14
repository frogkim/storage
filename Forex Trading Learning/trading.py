import numpy as np


class TRADING:
    def __init__(self, x_price, x_avg):
        self.x_price = x_price
        self.x_avg = x_avg
        self.startIndex = 0
        self.totalIndex = 99840 - 144

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

        self.step = 1e-5
        self.fee = 1e-5 * 20

    def SetGUI(self, gui):
        self.gui = gui

    def UpdateGUI(self):
        self.long = self.long_win + self.long_loss
        self.short = self.short_win + self.short_loss

        self.gui.SetBalance("{:0.4f}".format(self.balance))
        self.gui.SetDrawDown("{:0.2f} %".format(self.drawDown))
        self.gui.SetLong(self.long)
        self.gui.SetLongWin(self.long_win)
        self.gui.SetLongLoss(self.long_loss)

        self.gui.SetShort(self.short)
        self.gui.SetShortWin(self.short_win)
        self.gui.SetShortLoss(self.short_loss)

        if self.long > 0: self.gui.SetLongRate(("{:0.4f}".format(self.long_win / self.long)))
        if self.short > 0: self.gui.SetShortRate(("{:0.4f}".format(self.short_win / self.short)))

    def Reset(self, step):
        if self.long != 0 and self.short != 0:
            message = "Step : " + str(step)
            message += ", Balance : {:0.4f}".format(self.balance)
            message += ", DrawDown : {:0.2f}".format(self.drawDown)
            message += ", Long : {:0.4f}".format(self.long_win / self.long)
            message += ", Short : {:0.4f}".format(self.short_win / self.short)
            print(message)
            f = open("result.txt", "a")
            f.write(message)
            f.write("\n")
            f.close()

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
        profit = self.x_price[0, index + 1, 0] - self.x_price[0, index, 0]

        if state == 0:
            if action == 0:
                result -= self.step
            else:
                result -= self.fee
                result -= profit
                if -profit > 0:
                    self.short_win += 1
                else:
                    self.short_loss += 1

                if action == 2:
                    result -= self.fee

        elif state == 1:
            if action == 0:
                self.short += 1
                result -= self.fee
            elif action == 1:
                result -= self.step
            else:
                self.long += 1
                result -= self.fee

        else:
            if action == 2:
                result -= self.step
            else:
                result -= self.fee
                result += profit
                if profit > 0:
                    self.long_win += 1
                else:
                    self.long_loss += 1

                if action == 0:
                    result -= self.fee

        lot = int(self.balance / 1000) + 10
        self.balance += result * lot
        if self.maxBalance < self.balance: self.maxBalance = self.balance
        if self.minBalance > self.balance: self.minBalance = self.balance
        self.drawDown = ((self.maxBalance - self.minBalance) / self.maxBalance) * 100
        self.UpdateGUI()
        return result

    def Close(self, index, state):
        result = 0
        profit = self.x_price[0, index + 1, 0] - self.x_price[0, index, 0]

        if state == 0:
            result -= profit
            if -profit > 0:
                self.short_win += 1
            else:
                self.short_loss += 1
        else:
            result += profit
            if profit > 0:
                self.long_win += 1
            else:
                self.long_loss += 1
        return result