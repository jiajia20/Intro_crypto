import random as rd
import numpy as np

class node:

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth
        self.stake = 0
        self.risk = rd.random()
        self.blocks = 1
        self.stakers = {}

    def update(self, reward):
        self.wealth += reward
        self.blocks += 1
        self.risk *= 1.02

    def pity(self, amount):
        self.wealth += amount
        self.risk *= 0.98

    def participate(self, cost):
        self.stake = 0
        adjustment = 1
        while self.wealth > cost:
            if rd.random() > (self.risk / adjustment):
                break
            self.wealth -= cost
            self.stake += 1
            adjustment += 1
        return self.stake * cost

    def vote(self, node):
        node.stakers[self] = self.risk * self.wealth

    def sum_stakers(self):
        return sum(self.stakers.values())

class network:

    def __init__(self, num_nodes):
        self.nodes = []
        self.num_nodes = num_nodes
        self.normal_distribution()
        self.prize_pool = 0

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

    def participants(self, cost):
        self.prize_pool = 0
        participants = []
        for n in self.nodes:
            self.prize_pool += n.participate(cost)
            if (n.stake > 0):
                participants.append(n)
        return participants


