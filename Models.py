import random as rd
from pylab import *


"""
agents represent individual miners. 
They can 
    1)give tokens to stake
    2)receive reward for their staking
    3)receive random network reward

Agents are organized in a network whose topology can be altered. 
    1)can be used to model who delegate to who
    2)can be used in attack models

Since the real network usually contains about 80-90k max users, 
we model with ~100 agents for visualization and ~1k for simulation

"""


# create an agent with a mood with 
class agent:
        
    def __init__(self, i):
        self.tokens = random()*100  # bound (0,100)  round(random(),2)
        self.index= i
     
    def stake_give(self,pool,amount): #have their stake locked 
        self.tokens -= amount
        pool.tokens += amount #pool is a special kind of agent

    def stake_reward(self, amount): #reward after being selected (models the transaction fee earned) 
        self.tokens += amount
    
    def network_reward(self,amount): #reward from the network (models the block reward)
        self.token += amount


    
def initialize_network_agent(network):
    directory = {} 
    node_num = network.number_of_nodes()
    for i in range (node_num):
        directory.update({ i : agent(i)})
    return directory

