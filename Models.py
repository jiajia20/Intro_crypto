import random as rd
import numpy as np

class node:

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth
        self.blocks = 1

    def update(self, reward):
        self.wealth += reward
        self.blocks += 1

class network:

    def __init__(self, num_nodes):
        self.nodes = []
        self.num_nodes = num_nodes
        self.normal_distribution()

    def number_of_nodes(self):
        return self.num_nodes

    def gini_coefficient(self):
        """Compute Gini coefficient of array of values"""
        x = np.array([n.wealth for n in self.nodes])
        diffsum = 0
        for i, xi in enumerate(x[:-1], 1):
            diffsum += np.sum(np.abs(xi - x[i:]))
        return diffsum / (len(x)**2 * np.mean(x))

    def real_distribution(self):
        for low in range(int(self.num_nodes*0.8)):
            wealth = np.random.normal(loc=10, scale=2)
            self.nodes.append(node(low, wealth))
        for med in range(int(self.num_nodes*0.15)):
            wealth = np.random.normal(loc=100, scale=10)
            self.nodes.append(node(int(self.num_nodes*0.8)+med, wealth))
        for high in range(int(self.num_nodes*0.05)):
            wealth = 1000
            self.nodes.append(node(int(self.num_nodes*0.95)+high, wealth))

    def normal_distribution(self):
        for i in range(self.num_nodes):
            wealth = np.random.normal(loc=100, scale = 10)
            self.nodes.append(node(i, wealth))
