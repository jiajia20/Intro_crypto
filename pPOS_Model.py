import random as rd
import numpy as np

class player(object):

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth

    def update(self, block_reward, transaction_reward):
        self.wealth += block_reward + transaction_reward

class network:

    def __init__(self, num_nodes):
        self.nodes = []
        self.num_nodes = num_nodes
        self.block_reward = 5
        for i in range(num_nodes):
            wealth = np.random.normal(loc=10, scale=5)
            self.nodes.append(player(i, wealth))

    def number_of_nodes(self):
        return self.num_nodes

    def calc_centralization(self):
        x = np.array([n.wealth for n in self.nodes])

        """Compute Gini coefficient of array of values"""
        diffsum = 0
        for i, xi in enumerate(x[:-1], 1):
            diffsum += np.sum(np.abs(xi - x[i:]))
        return diffsum / (len(x)**2 * np.mean(x))