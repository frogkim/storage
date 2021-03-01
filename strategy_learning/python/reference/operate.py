import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import ctypes, time, datetime, os
import numpy as np
load = ctypes.cdll.LoadLibrary("./frozenfrog.dll")

SetTrigger = load.SetTrigger
SetTrigger.argtypes = [ctypes.c_int, ctypes.c_int,]
GetTrigger = load.GetTrigger
GetTrigger.argtypes = [ctypes.c_int, ]

SetValues = load.SetValues
SetValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,]
GetValues = load.GetValues
GetValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,]
GetValues.restype = ctypes.c_double

SetSignals = load.SetSignals
SetSignals.argtypes = [ctypes.c_int, ctypes.c_double,]
GetSignals = load.GetSignals
GetSignals.argtypes = [ctypes.c_int, ]
GetSignals.restype = ctypes.c_double

def multiply(input_X, input_rows, input_cols, output_cols):
    global number
    name='weight'+ str(number)
    var = tf.get_variable(name, shape=[input_cols, output_cols], dtype=tf.float64, initializer=tf.keras.initializers.glorot_uniform())
    name='bias'+ str(number)
    bia = tf.get_variable(name, shape=[input_rows, output_cols], dtype=tf.float64, initializer=tf.keras.initializers.glorot_uniform())
    number += 1
    r = tf.matmul(input_X, var) + bia
    return r

def Restore(saver, sess):
    if(os.path.isfile('./guiwin/model.index')):
        saver.restore(sess, './guiwin/model')
        print("restore success")
    else:
        init = tf.global_variables_initializer()
        sess.run(init)
        print("No Save File")

def Machine():

    setupList = np.zeros([5,120,28,15])
    for a in range(5):
        for b in range(120):
            for c in range(28):
                for d in range(5):
                    for e in range(3):
                        setupList[a,b,c,d*3 + e] = GetValues(a,b,c,d,e)

    input_dictionary = {X[0]:setupList[0],
                        X[1]:setupList[1],
                        X[2]:setupList[2],
                        X[3]:setupList[3],
                        X[4]:setupList[4]}

    hy_val = sess.run(hypothesis, feed_dict=input_dictionary)

    for a in range(28):
        for b in range(3):
            for c in range(3):
                SetSignals(a*3*3+b*3+c, hy_val[a,b,c])
    return

number = 0
Trigger = True
iteration = 0
curs = 28
rows = 120
cols = 15
neurons = 128

X  = []
for i in range(5):
    holdername = 'x-input' + str(i)
    X.append(tf.placeholder(tf.float64, [rows, curs, cols], name=holdername))


B = 0
for i in range(5):
    A = tf.reshape(X[i], [1, rows*curs*cols])
    A = multiply(A, 1, rows*curs*cols, neurons)
    A = multiply(A, 1,        neurons, neurons)
    B += A

B = multiply(B, 1, neurons, neurons)
B = multiply(B, 1, neurons, neurons)
C = multiply(B, 1, neurons, curs*3*3)
P = tf.reshape(C, [curs,3,3])

hypothesis = P

sess = tf.Session()
saver = tf.train.Saver()
Restore(saver, sess)

while(1):
    if(GetTrigger(0) == 0):
        time.sleep(0.1)
        continue
    Machine()
    SetTrigger(0,0)
    print(datetime.datetime.now())
