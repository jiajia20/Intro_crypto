from os import replace
import random as rd
import numpy as np
import collections

class protocol_interface:
    def validate_block(self, num_validators):
        """Choose a number of validators from the network and reward them"""
        pass

    def wealth_distribution(self):
        wealth_values = [n.wealth for n in self.network.nodes]
        total = sum(wealth_values)
        return [w/total for w in wealth_values]

    def reputation_distribution(self):
        repuation_values = [n.reputation() for n in self.network.nodes]
        total = sum(repuation_values)
        return [b/total for b in repuation_values]

    def delegate_distribution(self):
        delegate_values = [n.sum_stakers() for n in self.network.nodes]
        total = sum(delegate_values)
        return [s/total for s in delegate_values]

class pPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        # winner selected psudo-randomly with weight proportional to wealth
        probability_distribution = self.wealth_distribution()
        winners = list(np.random.choice(self.network.nodes, num_validators, p=probability_distribution, replace=False))
        for w in winners:
            reward = 20/num_validators
            w.add_wealth(reward)

class dPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        # each node votes for another node to be their delegate
        # nodes vote psudo-randomly with weight proportional to number of blocks validated times inverse of greed
        probability_distribution = self.reputation_distribution()
        election = np.random.choice(self.network.nodes, self.network.num_nodes, p=probability_distribution, replace=True)

        # each node stakes a certain amount of their wealth on their chosen delegate
        for i in range(len(self.network.nodes)):
            self.network.nodes[i].vote(election[i])

        # validator is chosen psudo-randomly with weight proportional to amount of wealth staked on them
        probability_distribution = self.delegate_distribution()
        winner = np.random.choice(self.network.nodes, 1, p=probability_distribution, replace=False)
        w = winner[0]

        # validator distributes block reward in accordance to their greed
        reward = 20
        winner_distribution = w.greed * reward
        staker_distribution = (1 - w.greed) * reward
        w.add_wealth(winner_distribution)
        w.add_blocks(1)

        # distribute wealth to stakers and each staker evaluates their opinion on the validator
        w_total = w.sum_stakers()
        for s, v in w.stakers.items():
            dist = v/w_total
            reward = staker_distribution * dist
            s.add_wealth(reward)
            s.opinion(w, reward)
        
        # clear the stakers and self reflect
        for n in self.network.nodes:
            n.stakers = {}
            n.reflect()


class lottery(protocol_interface):
    def __init__(self, network):
        self.network = network
        self.cost = 1
    
    def validate_block(self, num_validators):
        # each node decides whether or not to purchase "lottery tickets"
        participants = self.network.participants(self.cost)
        lottery_values = [n.stake for n in participants]
        total = sum(lottery_values)

        # network chooses winners without duplicate
        probability_distribution = [l/total for l in lottery_values]
        winners = list(np.random.choice(participants, num_validators, p=probability_distribution, replace=False))

        # set reward distribution ratio
        ratio = 10 * num_validators / self.network.num_nodes

        # distribute rewards, winners will get greedier
        winner_distribution = ratio * self.network.prize_pool
        winner_split = winner_distribution / num_validators
        for w in winners:
            w.add_wealth(winner_split)
            w.adjust_greed(1.05)

        # distribute consolation reward, losers get less greedy
        remainder = list(set(participants) - set(winners))
        remainder_distribution = (1.0 - ratio) * self.network.prize_pool
        remainder_split = remainder_distribution / len(remainder)
        for r in remainder:
            r.add_wealth(remainder_split)
            r.adjust_greed(0.99)
            if r.greed < 0.5:
                r.adjust_greed(1.5)
