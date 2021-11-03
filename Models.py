import random as rd
from pylab import *

"""
agents represent individual miners. 
They can 
    1)give tokens to stake
    2)receive reward for their staking
    3)receive random network reward

Agents are organized in a network whose topology ca be altered. 


In this simulation we have 500 - 2k miners in the simulation.


are set up to exchange tokens



, get rewarded and 
"""


# create an agent with a mood with 
class agent:
        
    def __init__(self, i):
        self.tokens = random()*100  # bound (0,100)  round(random(),2)
        self.index= i

        
    def stake_give(self,pool,amount):
        self.tokens -= amount
        pool.tokens += amount #pool is a special kind of agent

    def stake_reward(self, amount):
        self.tokens += amount
    
    def network_reward(self,amount):
        self.token += amount


    
def initialize_network_agent(network):
    directory = {} 
    node_num = network.number_of_nodes()
    for i in range (node_num):
        directory.update({ i : agent(i)})
    return directory




def run_sim(network, di, iters=100, mvy = 0, mry = 0):
    #make a storage list 
    mood_overtime = []
    for k in range(iters):
        mood_value = play(network, di, mvy, mry)
        mood_overtime.append(mean(mood_value))
        
    return mood_overtime   