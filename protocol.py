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

        for i in range(len(self.network.nodes)):
            self.network.nodes[i].vote(election[i])

        stake_values = [n.sum_stakers() for n in self.network.nodes]
        total_stake = sum(stake_values)
        stake_probability = [s/total_stake for s in stake_values]
        winner = np.random.choice(self.network.nodes, 1, p=stake_probability, replace=False)
        w = winner[0]

        reward = 20 + rd.randint(6,12)
        winner_distribution = 0.2 * reward
        staker_distribution = 0.8 * reward
        w.update(winner_distribution)

        w_total = w.sum_stakers()
        for s, v in w.stakers.items():
            dist = v/w_total
            s.pity(staker_distribution * dist)


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

        ratio = 10 * num_validators / self.network.num_nodes
        winner_distribution = ratio * self.network.prize_pool
        winner_split = winner_distribution / num_validators
        for w in winners:
            w.update(winner_split)

        remainder = list(set(participants) - set(winners))
        remainder_distribution = (1.0 - ratio) * self.network.prize_pool
        remainder_split = remainder_distribution / len(remainder)
        for r in remainder:
            r.pity(remainder_split)
