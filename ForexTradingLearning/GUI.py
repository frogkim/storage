import tkinter

import threading


class GUI:

    def __init__(self, name="main"):
        self.win = tkinter.Tk()
        self.win.title("Machine Learning")
        self.win.geometry("450x300+100+100")
        self.win.resizable(True, True)  # UpDown, LeftRight
        self.status = "Test message"
        self.exit = False

        # Save and Load Button
        self.btsave = tkinter.Button(self.win, text="Save", overrelief="solid", width=8,command=self._Save, repeatdelay=1000, repeatinterval=100)
        self.btload = tkinter.Button(self.win, text="Restore", overrelief="solid", width=8,command=self._Restore, repeatdelay=1000, repeatinterval=100)
        self.btinit = tkinter.Button(self.win, text="Initialze", overrelief="solid", width=8, command=self._Initialze, repeatdelay=1000, repeatinterval=100)

        self.btsave.place(x=20, y=250)
        self.btload.place(x=100, y=250)
        self.btinit.place(x=180, y=250)

        # Starts and Stop
        self.btstart = tkinter.Button(self.win, text="Start", overrelief="solid", width=8, command=self._Start, repeatdelay=1000, repeatinterval=100)
        self.btstop = tkinter.Button(self.win, text="Stop", overrelief="solid", width=8, command=self._Stop, repeatdelay=1000, repeatinterval=100)
        self.btstart.place(x=270, y=250)
        self.btstop.place(x=350, y=250)

        # Status
        self.lbStatus = tkinter.Label(self.win, text=self.status, width=43, height=1, bd=0, fg="black", bg='white', relief="solid")
        self.lbStatus.config(font=("Courier", 12))
        self.lbStatus.place(x=10, y=10)

        # Balance
        self.lbBalance = tkinter.Label(self.win, text="Balance : ", width=12, height=1, bd=0, fg="black",relief="solid")
        self.lbBalance.config(font=("Courier", 12))
        self.lbBalance.place(x=10, y=40)

        self.txBalance = tkinter.Label(self.win, text="0", width=30, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txBalance.config(font=("Courier", 12))
        self.txBalance.place(x=120, y=40)

        # Total
        self.lbTotal = tkinter.Label(self.win, text="Total : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbTotal.config(font=("Courier", 12))
        self.lbTotal.place(x=10, y=70)

        self.txTotal = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txTotal.config(font=("Courier", 12))
        self.txTotal.place(x=120, y=70)

        # Drawdown
        self.lbDrawDown = tkinter.Label(self.win, text="Drawdown : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbDrawDown.config(font=("Courier", 12))
        self.lbDrawDown.place(x=220, y=70)

        self.txDrawDown = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white', relief="solid")
        self.txDrawDown.config(font=("Courier", 12))
        self.txDrawDown.place(x=320, y=70)

        # Long
        self.lbLong = tkinter.Label(self.win, text="Long : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbLong.config(font=("Courier", 12))
        self.lbLong.place(x=15, y=100)

        self.txLong = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txLong.config(font=("Courier", 12))
        self.txLong.place(x=120, y=100)

        # LongWin
        self.lbLongWin = tkinter.Label(self.win, text="Win : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbLongWin.config(font=("Courier", 12))
        self.lbLongWin.place(x=15, y=130)

        self.txLongWin = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txLongWin.config(font=("Courier", 12))
        self.txLongWin.place(x=120, y=130)

        # LongLoss
        self.lbLongLoss = tkinter.Label(self.win, text="Loss : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbLongLoss.config(font=("Courier", 12))
        self.lbLongLoss.place(x=15, y=160)

        self.txLongLoss = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txLongLoss.config(font=("Courier", 12))
        self.txLongLoss.place(x=120, y=160)

        # LongRate
        self.lbLongRate = tkinter.Label(self.win, text="Rate : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbLongRate.config(font=("Courier", 12))
        self.lbLongRate.place(x=15, y=190)

        self.txLongRate = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txLongRate.config(font=("Courier", 12))
        self.txLongRate.place(x=120, y=190)

        # Short
        self.lbShort = tkinter.Label(self.win, text="Short : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbShort.config(font=("Courier", 12))
        self.lbShort.place(x=220, y=100)

        self.txShort = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white', relief="solid")
        self.txShort.config(font=("Courier", 12))
        self.txShort.place(x=320, y=100)

        # ShortWin
        self.lbShortWin = tkinter.Label(self.win, text="Win : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbShortWin.config(font=("Courier", 12))
        self.lbShortWin.place(x=220, y=130)

        self.txShortWin = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txShortWin.config(font=("Courier", 12))
        self.txShortWin.place(x=320, y=130)

        # ShortLoss
        self.lbShortLoss = tkinter.Label(self.win, text="Loss : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbShortLoss.config(font=("Courier", 12))
        self.lbShortLoss.place(x=220, y=160)

        self.txShortLoss = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txShortLoss.config(font=("Courier", 12))
        self.txShortLoss.place(x=320, y=160)

        # ShortRate
        self.lbShortRate = tkinter.Label(self.win, text="Rate : ", width=12, height=1, bd=0, fg="black", relief="solid")
        self.lbShortRate.config(font=("Courier", 12))
        self.lbShortRate.place(x=220, y=190)

        self.txShortRate = tkinter.Label(self.win, text="0", width=8, height=1, bd=0, fg="black", bg='white',relief="solid")
        self.txShortRate.config(font=("Courier", 12))
        self.txShortRate.place(x=320, y=190)

    def loop(self):
        self.win.protocol("WM_DELETE_WINDOW", self.Close)
        self.win.mainloop()

    def SetMachine(self, machine):
        self.machine = machine

    # exit event
    def Close(self):
        self.machine.TurnOff()
        self.machine.SetSwitch(-1)
        self.exit = True
        self.win.destroy()

    # start and stop
    def _CheckInit(self):
        if not self.machine.GetInitialize():
            self.status = "Not initialized"
            self.lbStatus.config(text=self.status)
            return False
        return True

    def _Start(self):
        check = self._CheckInit()
        if check is False: return
        message = self.machine.TurnOn(1)
        self.lbStatus.config(text=message)

    def _Stop(self):
        self.machine.Reset()
        message = self.machine.TurnOn(0)
        self.lbStatus.config(text=message)

    # save and restore
    def _Save(self):
        if not self._CheckInit(): return
        message = self.machine.Save()
        self.lbStatus.config(text=message)

    def _Restore(self):
        message = self.machine.Restore()
        self.lbStatus.config(text=message)

    def _Initialze(self):
        self.machine.Initialize()
        self.lbStatus.config(text="Initialization Done")

    def SetBalance(self,value):
        self.txBalance.config(text=value)

    def SetDrawDown(self,value):
        self.txDrawDown.config(text=value)

    def SetTotal(self,value):
        self.txTotal.config(text=value)

    def SetLong(self,value):
        self.txLong.config(text=value)

    def SetLongWin(self,value):
        self.txLongWin.config(text=value)

    def SetLongLoss(self,value):
        self.txLongLoss.config(text=value)

    def SetLongRate(self,value):
        self.txLongRate.config(text=value)

    def SetShort(self, value):
        self.txShort.config(text=value)

    def SetShortWin(self, value):
        self.txShortWin.config(text=value)

    def SetShortLoss(self, value):
        self.txShortLoss.config(text=value)

    def SetShortRate(self, value):
        self.txShortRate.config(text=value)
