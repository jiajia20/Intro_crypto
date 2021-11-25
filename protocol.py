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

    def block_distribution(self):
        block_values = [n.blocks for n in self.network.nodes]
        total = sum(block_values)
        return [b/total for b in block_values]

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
            reward = self.network.prize_pool/num_validators
            w.add_wealth(reward)

class dPOS(protocol_interface):
    def __init__(self, network):
        self.network = network

    def validate_block(self, num_validators):
        # each node votes for another node to be their delegate
        # nodes vote psudo-randomly with weight proportional to number of blocks validated
        probability_distribution = self.block_distribution()
        election = np.random.choice(self.network.nodes, self.network.num_nodes, p=probability_distribution, replace=True)

        # each node stakes a certain amount of their wealth on their chosen delegate
        for i in range(len(self.network.nodes)):
            self.network.nodes[i].vote(election[i])

        # validator is chosen psudo-randomly with weight proportional to amount of wealth staked on them
        probability_distribution = self.delegate_distribution()
        winner = np.random.choice(self.network.nodes, 1, p=probability_distribution, replace=False)
        w = winner[0]

        # validator distributes block reward in accordance to their greed
        reward = self.network.prize_pool
        winner_distribution = 0.25 * reward
        staker_distribution = 0.75 * reward
        w.add_wealth(winner_distribution)
        w.add_blocks(1)

        # distribute wealth to stakers and each staker evaluates their opinion on the validator
        w_total = w.sum_stakers()
        for s, v in w.stakers.items():
            dist = v/w_total
            reward = staker_distribution * dist
            s.add_wealth(reward)
        
        # clear the stakers and self reflect
        self.network.new_round()

class dPOS_GT(protocol_interface):
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
        reward = self.network.prize_pool
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
        self.network.new_round(True)

class ePOS(protocol_interface):

    def __init__(self, network):
        self.network = network
        self.blocks = network.create_blocks()
    
    # find the block with the greatest transaction
    # fee that does not exceed the node's current wealth
    def find_best_block(self, node, blocks):
        b = None
        for block in blocks:
            if node.wealth >= block.tf:
                if b is not None:
                    if block.tf > b.tf:
                        b = block
                else:
                    b = block
        
        return b

    def validate_block(self, num_validators):
        # setup potential miners for each block
        block_map = dict()
        for block in self.blocks:
            block_map[block] = []
    
        # find best block for each node
        for node in self.network.nodes:
            b = self.find_best_block(node, self.blocks)
            if b is not None:
                block_map[b].append(node)
        
        # 
        prev = []
        for block in block_map:

            # get list of potential miners
            potential_miners = block_map[block]

            # if miners voted, then pick one from previous blocks
            if len(potential_miners) == 0:
                potential_miners = prev

                # if none from previous blocks, pick random node
                if len(prev) == 0:
                    min_miner = self.network.find_rand_node()
                    min_miner.add_wealth(self.network.prize_pool)
                    min_miner.add_blocks(1)
                    continue
            
            # sort list of potential miners based on least blocks mined and then highest wealth
            potential_miners.sort(key=lambda m: (m.blocks, -m.wealth))

            # find miner and give reward (assuming honest validation)
            min_miner = potential_miners[0]
            min_miner.add_wealth(self.network.prize_pool)
            min_miner.add_blocks(1)
            
            # remove selected miner from potential list for future blocks
            if len(block_map[block]) != 0:
                potential_miners.remove(min_miner)
                for m in potential_miners:
                    prev.append(m)
            else:
                prev.remove(min_miner)

class lottery(protocol_interface):
    def __init__(self, network):
        self.network = network
        self.cost = 0.2
    
    def validate_block(self, num_validators):
        # each node decides whether or not to purchase "lottery tickets"
        participants = self.network.participants(self.cost)
        lottery_values = [n.stake for n in participants]
        total = sum(lottery_values)

        # network chooses winners without duplicate
        probability_distribution = [l/total for l in lottery_values]
        winners = list(np.random.choice(participants, num_validators, p=probability_distribution, replace=False))

        # set reward distribution ratio
        w_ratio = min(5 * num_validators / len(participants), .90)

        # distribute rewards, winners will get 10% greedier if they made money
        # if they lose money, they get 10% less greedy
        winner_distribution = w_ratio * self.network.prize_pool
        winner_split = winner_distribution / num_validators
        for w in winners:
            w.add_wealth(winner_split)
            if (winner_split > w.stake * self.cost):
                w.adjust_greed(1.1)
            else:
                w.adjust_greed(0.90)

        remaining_reward = (1 - w_ratio) * self.network.prize_pool

        remainder = list(set(participants) - set(winners))
        non_participants = list(set(self.network.nodes) - set(participants))

        p_ratio = min(len(participants) / len(non_participants), .9)

        # distribute consolation reward, if the node makes money, increase their greed by 2%
        # if they lose money, they get 5% less greedy to compensate for loss
        remainder_distribution = p_ratio * remaining_reward
        remainder_split = remainder_distribution / len(remainder)
        for r in remainder:
            r.add_wealth(remainder_split)
            if (remainder_split > r.stake * self.cost):
                r.adjust_greed(1.02)
            else:
                r.adjust_greed(0.95)

        # distribute a small amount to non-participants
        # increase greed by 1% each round for "FOMO"
        non_part_distribution = (1 - p_ratio) * remaining_reward
        non_part_split = non_part_distribution / len(non_participants)
        for n in non_participants:
            n.add_wealth(non_part_split)
            n.adjust_greed(1.01)

        self.network.new_round()