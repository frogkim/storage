--- Future plan ---  
1. To change learning algorithm as LSTM  
2. To change finding action algorithm as Q-learning  
(done) To apply softmax to predict value  
(done) To apply minibatch  

- Updates in Mar.4.2021  
1. adjustment about "python"  
  Softmax function is applied
  minibatch is applied  
  dataloading() in function.py is changed.  
  avg array consists of [99840 - 144 - 11, 120]. Each currency data is concatenated to the same row.  
  ans array consists of [99840 - 144 - 11, 3(states), 3(actions)].  
  144 and 11 is caused that avg's maximum period is 144, and ans is made by consecutive 11 timeframe.  

2. "avg" is chagned  
  This code generates [99840 - 144, 120] data sets.

- Updates in Feb.28.2021
1. "mql5 and communicatie" communicate each other with "frozendll."

  frozendll.dll is to provide shared memory.
  mql5 is run in Metaquete5. Metaquete5 uses its original langauge mql5. It is based on old stype c++.
  mql5 receives prices data from the broker's server and send them to communicate with frozendll.dll.
  communicate receives data from mql5 and saves them on disk. It makes totally 6 files, *.dat.
  "*.dat" files are written with binary types. It is good to save storage and reduce time to load.
  
2. "avg" makes analying data.

  This program reads *.dat files, calculates average lines of open, high, low, close prices with period 3, 8, 21, 55, 144.
  In one timeline, there are 20 lines each currencies.
  Then, it calculates "value = (average - prices) / average" and save.
  The machine will learn with this value, not original prices.

3. "python" is machine learning with Tensorflow
  GUI.py has gui statements
  MACHINE.py has machine learning statements.
  MACHINE.py imports functions from fucntion.py.
  In function.py, there are about loarding prices data.
  
