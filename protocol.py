from os import replace
import random as rd
import numpy as np
import collections

class protocol_interface:
    def validate_block(self, num_validators):
        """Choose a number of validators from the network and reward them"""
        pass

    def reward_winners(self, winners):
        for w in winners:
            reward = 20 + rd.randint(6,12)
            w.update(reward)


class pPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        wealth_values = [n.wealth for n in self.network.nodes]
        total = sum(wealth_values)

        # winner selected psudo-randomly with weight proportional to wealth
        probability_distribution = [w/total for w in wealth_values]
        winners = list(np.random.choice(self.network.nodes, num_validators, p=probability_distribution, replace=False))
        self.reward_winners(winners)

class dPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        block_values = [n.blocks for n in self.network.nodes]
        total = sum(block_values)

        # each node votes for another node to be a validator
        # nodes vote psudo-randomly with weight proportional to number of blocks validated
        probability_distribution = [b/total for b in block_values]
        election = np.random.choice(self.network.nodes, self.network.num_nodes, p=probability_distribution, replace=True)
        top_votes = collections.Counter(election).most_common(num_validators)
        winners = [n[0] for n in top_votes]
        self.reward_winners(winners)

class lottery(protocol_interface):
    def __init__(self, network):
        self.network = network
        self.cost = 1
    
    def validate_block(self, num_validators):
        participants = self.network.participants(self.cost)
        lottery_values = [n.stake for n in participants]
        total = sum(lottery_values)

        ## each node decides whether or not to purchase "lottery tickets"
        ## network chooses winners without duplicate
        probability_distribution = [l/total for l in lottery_values]
        winners = list(np.random.choice(participants, num_validators, p=probability_distribution, replace=False))

        ratio = 5 * num_validators / self.network.num_nodes
        winner_distribution = ratio * self.network.prize_pool
        winner_split = winner_distribution / num_validators
        for w in winners:
            w.update(winner_split)

        remainder = list(set(participants) - set(winners))
        remainder_distribution = (1.0 - ratio) * self.network.prize_pool
        remainder_split = remainder_distribution / len(remainder)
        for r in remainder:
            r.pity(remainder_split)
