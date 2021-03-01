import random
import sys
import numpy as np

rows = 300000
curs = 28
cols = 75


def FileSetup():
    file_currency = "../strategy/train3.dat"
    fc = open(file_currency, "rb")
    a = np.fromfile(fc, dtype=np.float64, count=-1, sep="", offset=0)
    a = a.reshape([rows, curs, cols])
    return a

def ArraySetup(avg):
    x1_input = np.zeros([rows, curs, 15])
    x2_input = np.zeros([rows, curs, 60])

    for i in range(rows):
        for j in range(curs):
            for k in range(15):
                x1_input[i,j,k] = avg[i, j, k]
            for k in range(60):
                x2_input[i,j,k] = avg[i, j, k+15]

    return x1_input, x2_input

filename_x1_input = "./samples/x1_input.dat"
filename_x2_input = "./samples/x2_input.dat"

fx1 = open(filename_x1_input, "wb")
fx2 = open(filename_x2_input, "wb")

avg = FileSetup()
x1_input, x2_input = ArraySetup(avg)


x1_input.tofile(fx1)
x2_input.tofile(fx2)
#y_input.tofile(fy)
fx1.close()
fx2.close()
#fy.close()
















    
