import random
import sys
import numpy as np


def FileString(cur_num):

    if(cur_num == 0): return "eurusd"
    if(cur_num == 1): return "gbpusd"
    if(cur_num == 2): return "audusd"
    if(cur_num == 3): return "usdchf"
    if(cur_num == 4): return "usdcad"
    if(cur_num == 5): return "usdjpy"

def SetupPrice(cur_num):
    rows = 99840
    cols = 4
    filename = "../data/" + FileString(cur_num) + ".dat"
    f = open(filename, "rb")
    price = np.fromfile(f, dtype=np.float64, count=-1, sep="", offset=0)
    price = price.reshape([rows, cols])
    f.close()
    return price

def SetupAVG():
    rows = 99840-144
    cols = 20 * 6
    filename = "../data/" + "avg.dat"
    f = open(filename, "rb")
    avg = np.fromfile(f, dtype=np.float64, count=-1, sep="", offset=0)
    avg = avg.reshape([rows, cols])
    f.close()
    return avg

def SetupANS(cur_num):
    rows = 99840-11
    cols = 3
    filename = "../data/" + "ans" + FileString(cur_num) + ".dat"
    f = open(filename, "rb")
    ans = np.fromfile(f, dtype=np.int32, count=-1, sep="", offset=0)
    ans = ans.reshape([rows, cols])
    f.close()
    return ans
