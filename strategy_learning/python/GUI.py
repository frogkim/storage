import tkinter

import threading

class GUI:

    def __init__(self, name="main"):
        self.turnon = False
        self.initialize = False
        
        self.win = tkinter.Tk()
        self.win.title("Machine Learning")
        self.win.geometry("450x300+100+100")
        self.win.resizable(True, True) #UpDown, LeftRight
        self.status = "Test message"
        self.exit = False


        # Save and Load Button
        self.btsave = tkinter.Button(self.win, text = "Save", overrelief="solid", width=8,
                                    command=self._Save, repeatdelay=1000, repeatinterval=100)
        self.btsave.place(x=20, y=170)

        self.btload = tkinter.Button(self.win, text = "Restore", overrelief="solid", width=8,
                                   command=self._Restore, repeatdelay=1000, repeatinterval=100)
        self.btload.place(x=100, y=170)

        self.btinit = tkinter.Button(self.win, text = "Initialze", overrelief="solid", width=8,
                                   command=self._Initialze, repeatdelay=1000, repeatinterval=100)
        self.btinit.place(x=180, y=170)

        # Starts and Stop
        self.btstart = tkinter.Button(self.win, text = "Start1", overrelief="solid", width=8,
                                    command=self._Start1, repeatdelay=1000, repeatinterval=100)
        self.btstart.place(x=270, y=170)

        self.btstart2 = tkinter.Button(self.win, text = "Start2", overrelief="solid", width=8,
                                    command=self._Start2, repeatdelay=1000, repeatinterval=100)
        self.btstart2.place(x=270, y=200)

        self.btstart3 = tkinter.Button(self.win, text = "Start3", overrelief="solid", width=8,
                                    command=self._Start3, repeatdelay=1000, repeatinterval=100)
        self.btstart3.place(x=270, y=230)

        self.btstop = tkinter.Button(self.win, text = "Stop", overrelief="solid", width=8,
                                   command=self._Stop, repeatdelay=1000, repeatinterval=100)
        self.btstop.place(x=350, y=200)

        # Status
        self.lbStatus = tkinter.Label(self.win, text=self.status, width=43, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.lbStatus.config(font=("Courier", 12))
        self.lbStatus.place(x=10, y=10)

        # Labels
        self.AccLabel = tkinter.Label(self.win, text="Accuracy : ", width=12, height=1, bd = 0, fg="black", relief="solid")
        self.AccLabel.config(font=("Courier", 12))
        self.AccLabel.place(x=10, y=40)

        self.AccText = tkinter.Label(self.win, text="0", width=30, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.AccText.config(font=("Courier", 12))
        self.AccText.place(x=120, y=40)

        # Labels2
        self.AccLabel2 = tkinter.Label(self.win, text="loss : ", width=12, height=1, bd = 0, fg="black", relief="solid")
        self.AccLabel2.config(font=("Courier", 12))
        self.AccLabel2.place(x=10, y=70)

        self.AccText2 = tkinter.Label(self.win, text="0", width=30, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.AccText2.config(font=("Courier", 12))
        self.AccText2.place(x=120, y=70)

        # Labels3
        self.AccLabel3 = tkinter.Label(self.win, text="Total : ", width=12, height=1, bd = 0, fg="black", relief="solid")
        self.AccLabel3.config(font=("Courier", 12))
        self.AccLabel3.place(x=10, y=100)

        self.AccText3 = tkinter.Label(self.win, text="0", width=8, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.AccText3.config(font=("Courier", 12))
        self.AccText3.place(x=120, y=100)


        # Labels Turn
        self.Turn = tkinter.Label(self.win, text="Turn : ", width=12, height=1, bd = 0, fg="black", relief="solid")
        self.Turn.config(font=("Courier", 12))
        self.Turn.place(x=220, y=100)

        self.txTurn = tkinter.Label(self.win, text="0", width=8, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.txTurn.config(font=("Courier", 12))
        self.txTurn.place(x=320, y=100)

        # Labels5
        self.Short = tkinter.Label(self.win, text="Short :", width=6, height=1, bd = 0, fg="black", relief="solid")
        self.Short.config(font=("Courier", 10))
        self.Short.place(x=20, y=130)

        self.txShort = tkinter.Label(self.win, text="0", width=6, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.txShort.config(font=("Courier", 10))
        self.txShort.place(x=90, y=130)
        # Labels6
        self.Empty = tkinter.Label(self.win, text="Netr :", width=6, height=1, bd = 0, fg="black", relief="solid")
        self.Empty.config(font=("Courier", 10))
        self.Empty.place(x=160, y=130)

        self.txEmpty = tkinter.Label(self.win, text="0", width=6, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.txEmpty.config(font=("Courier", 10))
        self.txEmpty.place(x=230, y=130)
        # Labels7
        self.Long = tkinter.Label(self.win, text="Long :", width=6, height=1, bd = 0, fg="black", relief="solid")
        self.Long.config(font=("Courier", 10))
        self.Long.place(x=300, y=130)

        self.txLong = tkinter.Label(self.win, text="0", width=6, height=1, bd = 0, fg="black", bg='white', relief="solid")
        self.txLong.config(font=("Courier", 10))
        self.txLong.place(x=370, y=130)

        
    def loop(self):
        self.win.protocol("WM_DELETE_WINDOW", self.Close)
        self.win.mainloop()

    #exit event
    def Close(self):
        self.machine.switch = 0
        self.exit = True
        self.win.destroy()
    
    def SetMachine(self, machine):
        self.machine = machine

    # start and stop
    def _CheckInit(self):
        if not self.initialize:
            self.status = "Not initialized"
            self.lbStatus.config(text=self.status)
            return False
        return True
    
    def _Start1(self):
        check = self._CheckInit()
        if(check is False): return
        message = self.machine.turnon(1)
        self.lbStatus.config(text=message)

    def _Start2(self):
        check = self._CheckInit()
        if(check is False): return
        message = self.machine.turnon(2)
        self.lbStatus.config(text=message)

    def _Start3(self):
        check = self._CheckInit()
        if(check is False): return
        message = self.machine.turnon(3)
        self.lbStatus.config(text=message)

    def _Stop(self):
        self.machine.reset()
        message = self.machine.turnon(0)
        self.lbStatus.config(text=message)

    # save and restore
    def _Save(self):
        if not self.initialize:
            self.status = "Not initialized"
            self.lbStatus.config(text=self.status)
            return
        message = self.machine.save()
        self.lbStatus.config(text=message)

    def _Restore(self):
        message = self.machine.restore()
        self.lbStatus.config(text=message)

    def _Initialze(self):
        self.machine.initialize()
        self.lbStatus.config(text="Initialization Done")
      
        
        
