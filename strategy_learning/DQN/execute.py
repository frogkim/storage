# Need to be installed Tensorflow v2 or upper, Numpy
# This code contains GUI class and MACHINE class
# GUI class controls buttons, texts, and labels
# MACHINE class controls machine learning part.

import random, ctypes, time, os, tkinter, sys
import numpy as np
import threading

from GUI import GUI
from machine import MACHINE
# from function import NoSetup, FileString

def main():
    # create each instances
    machine = MACHINE()
    gui = GUI()

    # send instances each other to communicate
    machine.SetGUI(gui)
    gui.SetMachine(machine)

    # operate with seperate thread
    my_thread = threading.Thread(target=machine.Operate)
    my_thread.start()
    my_thread2 = threading.Thread(target=gui.loop())
    my_thread2.start()


if __name__ == "__main__":
    main()
    exit()
