# I. Making Data  
This is to make input data for Forex Trading Machine.  
Via dll file, it shares memory map with MetaTrader5 and collect prices data.
Prices data are "EURUSD", "GBPUSD", "AUDUSD", "USDCHF, ""USDJPY", and "USDCAD."  
It calculates 5 simple average lines and ratio of between open price and average line.  
Finally, it creates avg.dat file.

# II. Forex Trading Machine
## Summary  

Input six difference currency pairs. The machine interprets states with LSTM, and decides its position.
Result is stored, and the machine is learned by its data with Q-learning.  

execute.py  
    - Main function. Create gui and machine object  

GUI.py  
    - GUI class    
    - Show progress and control machine operation.  

machine.py  
    - Create neural-net object and trading object  
    - Collect input data and command orders about machine learning  
    - Predict optimize action and test via trading object  
    - Update neural nets with Q-learning algorithm  
    - When predicting, it uses target Network but when updating, it uses main Network  
    - Target Network copies neurals of main Network when five steps updates are ended.  
  
neurals.py  
    - Create neural-net Tensors  
    - Receive input data from machine object and operate learning process with LSTM algorithm  

trading.py  
    - Calculate profit and loss when the machine opens or closes position  
    - Update result data and store as text file  

### 1. Structure
![Neural Net](https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/structure.png)  
There are two neural networks, target and main.
        
        <neurals.py>
        # This code do not use tensorflow's lstm module
        # to customize lstm algorism easily
        def _LSTM(self, i_data, short, long, w_list, b_list):
            i_t = tf.matmul(i_data, w_list[0]) + tf.matmul(short, w_list[1]) + b_list[0]
            i_t = tf.nn.sigmoid(i_t)
            f_t = tf.matmul(i_data, w_list[2]) + tf.matmul(short, w_list[3]) + b_list[1]
            f_t = tf.nn.sigmoid(f_t)
            o_t = tf.matmul(i_data, w_list[4]) + tf.matmul(short, w_list[5]) + b_list[2]
            o_t = tf.nn.sigmoid(o_t)
            g_t = tf.matmul(i_data, w_list[6]) + tf.matmul(short, w_list[7]) + b_list[3]
            g_t = tf.nn.tanh(g_t)
    
            long = f_t * long + i_t * g_t
            short = o_t * tf.nn.tanh(long)
            o_data = short
            return o_data, short, long

        <machine.py>
        # The machine predict rewards with target network and store in Q_stack
        prediction = self.targetDQN.Predict(x_stack)
        q_stack[i, action] = reward
        
        # The machine optimize Q_stack with bellman equation backward
        for i in range(oneGameTime - 2, -1):
            reward_next = np.max(q_stack[i + 1])
            q_stack[i, actions[i]] += gamma * reward_next        

        # The machin update main network (graph is for tensorboard)
        _, _, graph = self.mainDQN.Update(x_stack, y_stack)

        # Target network copies nuerals of main network very 200 updates end
        if self.count == 200:
            self.targetDQN.Copy(self.mainDQN)        

### 2. Application screen
![GUI](https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/dqn.png)    
  tkinter is used for gui interface. It helps to control machine conveniently.  

### 3. Reulst
![Result Text](https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/result.png)  
![Result Tensorboard](https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/tensorboard.png)  
Trading result looks bad, but getting better.  
Its profit is negative, but balance grows gradually.  

![Result Gragh](https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/result2.png)  
However, it is the result by reducing opening training.    


### 4. Conclusion  
It is confirmed that machine is learning. However, machine's action is different with intened action.  
Goal is to make profit, but the machine's choice is to do nothing.





### Reference  
Mnih, V., Kavukcuoglu, K., Silver, D. et al.  Human-level control through deep reinforcement learning. Nature 518, 529–533 (2015).  
https://doi.org/10.1038/nature14236
            
            Algorithm 1: deep Q-learning with experience replay
            Initialize replay memory D to capacity N
            Initialize action-value function  with random weights θ
            Initialize target action-value function  with weights θ^− = θ
            
            For episode = 1, M do
                Initialize sequence s_1 = {x_1} and preprocessed sequence Φ_1 = Φ(s_1)
                For t = 1,T do
                    With probability ε select a random action a_t
                    otherwise select a_t = argmax_a Q(Φ(s_t), a; theta)
                    Execute action at in emulator and observe reward rt and image x_t+1
                    Set s_t+1 = s_t, a_t, x_t+1 and preprocess 
                    Store transition (Φ_t, a_t, r_t, Φ_t+1) in D
                    Sample random minibatch of transitions(Φ_t, a_t, r_t, Φ_t+1) from D
                    Set 
                             y_j = r_j 						if episode termnmiates ate step j+1
                    or	 y_j = r_j + gamma * max_d Q^ (Φ_j+1, a'; θ^−)		otherwise
            
                    Perform a gradient descent step on (y_j - Q(Φ_j, a_j ; θ) )^2
                    with respect to the network parameters θ
                    Every C steps reset Q^ = Q
                End For
            End For            
            
