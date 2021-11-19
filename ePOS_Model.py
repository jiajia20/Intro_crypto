import numpy as np

class player(object):

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth
        self.blocks_mined = 0

    def update(self, block_reward, transaction_reward):
        self.wealth += block_reward + transaction_reward
        self.blocks_mined += 1

class network(object):

    def __init__(self, num_nodes):
        self.nodes = []
        self.num_nodes = num_nodes
        self.block_reward = 20
        for i in range(num_nodes):
            wealth = np.random.normal(loc=100, scale=10)
            self.nodes.append(player(i, wealth))

        self.nodes.sort(key=lambda n: n.wealth)

    def number_of_nodes(self):
        return self.num_nodes

    def calc_centralization(self):
        """Compute Gini coefficient of array of values"""
        x = np.array([n.wealth for n in self.nodes])
        diffsum = 0
        for i, xi in enumerate(x[:-1], 1):
            diffsum += np.sum(np.abs(xi - x[i:]))
        return diffsum / (len(x)**2 * np.mean(x))
    
    def create_blocks(self):
        blocks = []
        num_blocks = np.random.randint(1, 10)
        for i in range(num_blocks):
            blocks.append(block(self))
        blocks.sort(key=lambda b: b.tf, reverse=True)
        return blocks

    def find_min_max_wealth(self):
        self.nodes.sort(key=lambda n: n.wealth)
        return self.nodes[0].wealth, self.nodes[-1].wealth

    def find_rand_node(self):
        node_loc = np.random.randint(0, self.number_of_nodes())
        return self.nodes[node_loc]

class block(object):

    def __init__(self, network):
        min_wealth, max_wealth = network.find_min_max_wealth()
        self.tf = np.random.random() * max_wealth/2


    