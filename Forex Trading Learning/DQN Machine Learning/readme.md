# Forex Trading Machine
## Abstract 

Input six difference currency pairs. The machine interprets states with LSTM, and decides its position.
Result is stored, and the machine is learned by its data with Q-learning.

1. Structure
2. Application screen
3. Result
4. Conclusion

### 1. Structure

<img src="https://github.com/frogkim/publishdata/blob/main/images/ForexTradingLearning/structure.png">

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
            