from os import replace
import random as rd
import numpy as np
import collections

class protocol_interface:
    def validate_block(network, num_validators):
        """Choose a number of validators from the network and reward them"""
        pass


class pPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        wealth_values = [n.wealth for n in self.network.nodes]
        total = sum(wealth_values)

        # winner selected psudo-randomly with weight proportional to wealth
        probability_distribution = [w/total for w in wealth_values]
        winners = list(np.random.choice(self.network.nodes, num_validators, p=probability_distribution, replace=False))
        for w in winners:
            reward = 20 + rd.randint(6,12)
            w.update(reward)

class dPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        block_values = [n.blocks for n in self.network.nodes]
        total = sum(block_values)

        # each node votes for another node to be a validator
        # nodes vote psudo-randomly with weight proportional to number of blocks validated
        probability_distribution = [w/total for w in block_values]
        election = np.random.choice(self.network.nodes, self.network.num_nodes, p=probability_distribution, replace=True)
        top_votes = collections.Counter(election).most_common(num_validators)
        winners = [n[0] for n in top_votes]
        for w in winners:
            reward = 20 + rd.randint(6,12)
            w.update(reward)