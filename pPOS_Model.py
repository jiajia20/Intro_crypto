import random as rd
import numpy as np

class player(object):

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth

    def update(self, reward):
        self.wealth += reward

class network:

    def __init__(self, num_nodes, distribution):
        self.nodes = []
        self.num_nodes = num_nodes
        for i in range(num_nodes):
            wealth = np.random.normal(loc=100, scale=10)
            self.nodes.append(player(i, wealth))

    def number_of_nodes(self):
        return self.num_nodes

    def calc_centralization(self):
        return 0