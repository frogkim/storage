import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import random, ctypes, time, os, tkinter, sys
import numpy as np
from function import NoSetup, FileString
import threading

def multiply(input_X, input_rows, input_cols, output_cols):
    global number
    name='weight'+ str(number)
    var = tf.get_variable(name, shape=[input_cols, output_cols], dtype=tf.float64, initializer=tf.keras.initializers.glorot_uniform())
    name='bias'+ str(number)
    bia = tf.get_variable(name, shape=[input_rows, output_cols], dtype=tf.float64, initializer=tf.keras.initializers.glorot_uniform())
    number += 1
    r = tf.matmul(input_X, var) + bia
    return r


def RenewText(y):
    global iteration, step, acc, pas, tot, cost_avg, iterate, hy_count, hy_val
    StepText.config(text=str(step))
    CostText.config(text=str(round(cost_avg/step,8)))
    for i in range(28):
        for j in range(3):
            maximum = np.argmax(hy_val[i][j])
            answer = np.argmax(y[i][j])
            if(maximum == answer): acc+=1

            if(y[i][j][0] == 1): 
                hy_count[i][j][0] += 1
                hy_list[i][j][0].config(text=str(int(hy_count[i][j][0])))
            elif(y[i][j][1] == 1): 
                hy_count[i][j][1] += 1
                hy_list[i][j][1].config(text=str(int(hy_count[i][j][1])))
            elif(y[i][j][2] == 1): 
                hy_count[i][j][2] += 1
                hy_list[i][j][2].config(text=str(int(hy_count[i][j][2])))
    AccText.config(text=str(round(acc/(84*step),8)))

    if(step == 10000):
        sys.stdout.write("iteration : %d, acc : %0.6f, cost : %0.12f\n"%(iteration, acc/(84*step), cost_avg/step))
        sys.stdout.flush()
        iteration += 1
        step = 0
        acc = 0
        pas = 0
        tot = 0
        cost_avg = 0
        hy_count = np.zeros([curs,3,3])
        IterText.config(text=str(round(iteration)))
        for i in range(28):
            for j in range(3):
                for k in range(3):
                    hy_list[i][j][k].config(text=str(0))

def Restore(saver, sess):
    if(os.path.isfile('./guiwin/model.index')):
        saver.restore(sess, './guiwin/model')
        print("restore success")
    else:
        init = tf.global_variables_initializer()
        sess.run(init)
        print("No Save File")

def Stop():
    global Trigger
    Trigger = True
    print("Button turned off")

def Start():
    global step, acc, pas, tot, cost_avg, iterate, hy_val, Trigger
    Trigger = False
    step = 0
    acc = 0
    pas = 0
    tot = 0
    cost_avg = 0
    iterate = 0
    print("Button turned on")

def Machine():
    global step, acc, pas, tot, cost_avg, iterate, Trigger, hy_val, setupList
    check = 0
    number_i = 0
    number_j = 0
    while(1):
        if(Trigger):
            time.sleep(1)
            continue
        index = random.randrange(300000-rows)

        if(number_j == 3): 
            number_i += 1
            number_j = 0
        if(number_i == 28): number_i = 0

        input_dictionary = {X[0]:setupList[0][index:index+rows][:][:],
                            X[1]:setupList[1][index:index+rows][:][:],
                            X[2]:setupList[2][index:index+rows][:][:],
                            X[3]:setupList[3][index:index+rows][:][:],
                            X[4]:setupList[4][index:index+rows][:][:],
                               Y:setupList[5][index][:][:][:]}


        quatation = check%3
        
        if(quatation == 0):
            if(setupList[5][index][number_i][number_j][0] == 1):
                check += 1
                number_j += 1
                #if(number_j == 0):continue
            else: continue
        elif(quatation == 1):
            if(setupList[5][index][number_i][number_j][1] == 1):
                check += 1
                number_j += 1
                #if(number_j == 1):continue
            else: continue
        else:
            if(setupList[5][index][number_i][number_j][2] == 1):
                check += 1
                number_j += 1
                #if(number_j == 2):continue

        _, cost_val, hy_val = sess.run([train, cost, hypothesis], feed_dict=input_dictionary)

        step += 1
        tot += 1
        cost_avg += cost_val
        RenewText(setupList[5][index])
        if(step%1000==0):
           save_path = saver.save(sess, "./guiwin/model")
           if(step%100000==0):
               save_path = saver.save(sess, "./guiwin/100000/model")
               if(step%1000000==0):
                   save_path = saver.save(sess, "./guiwin/1000000/model")
    return

number = 0
Trigger = True
iteration = 0
curs = 28
rows = 120
cols = 15
neurons = 128

step = 0
acc = 0
pas = 0
tot = 0
cost_avg = 0
iterate = 0
hy_count = np.zeros([curs,3,3])
hy_val = np.zeros([curs,3,3])

setupList = NoSetup()

X  = []
for i in range(5):
    holdername = 'x-input' + str(i)
    X.append(tf.placeholder(tf.float64, [rows, curs, cols], name=holdername))

Y  = tf.placeholder(tf.float64, [curs,3,3], name='y-input')
Z  = 1e-4

optimizer = tf.train.RMSPropOptimizer(learning_rate = Z)


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
xentropy = tf.square(Y - hypothesis)

cost = tf.reduce_mean(xentropy)
train = optimizer.minimize(cost)

sess = tf.Session()
saver = tf.train.Saver()
Restore(saver, sess)



win = tkinter.Tk()
win.title("Machine Learning")
win.geometry("850x800+100+100")
win.resizable(True, True) #UpDown, LeftRight

currency = []
for i in range(28):
    currency.append(tkinter.Label(win, text=FileString(i), width=8, height=1, bd = 1, fg="black", relief="solid"))
for i in range(28):
    height = 80 + i*25
    currency[i].place(x=10, y=height)

hy_list = []
for i in range(28):
    tmp = []
    for j in range(3):
        tmp2 = []
        for k in range(3):
            tmp2.append(tkinter.Label(win, text=0, width=8, height=1, bd = 1, fg="black", bg='white', relief="solid"))
        tmp.append(tmp2)
    hy_list.append(tmp)

for i in range(28):
    y_axis = 80 + i*25
    for j in range(3):
        for k in range(3):
            x_axis = 90 + 230*j + 70*k
            hy_list[i][j][k].place(x=x_axis, y=y_axis)

start = tkinter.Button(win, text = "Start", overrelief="solid", width=8, command=Start, repeatdelay=1000, repeatinterval=100)
start.place(x = 10, y = 10)

stop = tkinter.Button(win, text = "Stop", overrelief="solid", width=8, command=Stop, repeatdelay=1000, repeatinterval=100)
stop.place(x = 110, y = 10)

IterLabel = tkinter.Label(win, text="Iteration : ", width=16, height=1, bd = 0, fg="black", relief="solid")
IterLabel.config(font=("Courier", 14))
IterLabel.place(x=200, y=10)

IterText = tkinter.Label(win, text="0", width=12, height=1, bd = 0, fg="black", bg='white', relief="solid")
IterText.config(font=("Courier", 12))
IterText.place(x=380, y=10)


StepLabel = tkinter.Label(win, text="Step : ", width=8, height=1, bd = 0, fg="black", relief="solid")
StepLabel.config(font=("Courier", 14))
StepLabel.place(x=10, y=45)

StepText = tkinter.Label(win, text="0", width=12, height=1, bd = 0, fg="black", bg='white', relief="solid")
StepText.config(font=("Courier", 12))
StepText.place(x=90, y=45)

AccLabel = tkinter.Label(win, text="Accuracy : ", width=12, height=1, bd = 0, fg="black", relief="solid")
AccLabel.config(font=("Courier", 14))
AccLabel.place(x=240, y=45)

AccText = tkinter.Label(win, text="0", width=12, height=1, bd = 0, fg="black", bg='white', relief="solid")
AccText.config(font=("Courier", 12))
AccText.place(x=370, y=45)

CostLabel = tkinter.Label(win, text="Cost : ", width=8, height=1, bd = 0, fg="black", relief="solid")
CostLabel.config(font=("Courier", 14))
CostLabel.place(x=520, y=45)

CostText = tkinter.Label(win, text="0", width=12, height=1, bd = 0, fg="black", bg='white', relief="solid")
CostText.config(font=("Courier", 12))
CostText.place(x=600, y=45)


my_thread = threading.Thread(target=Machine)
my_thread.start()

win.mainloop()
