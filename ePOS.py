import numpy as np
from time import sleep
from copy import deepcopy

'''
extended PoS
https://ieeexplore.ieee.org/abstract/document/9312484


'''

def find_best_block(node, blocks):
    b = None
    for block in blocks:
        if node.wealth >= block.tf:
            if b is not None:
                if block.tf > b.tf:
                    b = block
            else:
                b = block
    
    return b

def find_min_miner(potential_miners):
    miner_list = [potential_miners[0]]

    min_miner = potential_miners[0]
    for miner in potential_miners[1:]:
        if miner.blocks_mined == min_miner.blocks_mined:
            miner_list.append(miner)
        elif miner.blocks_mined < min_miner.blocks_mined:
            miner_list.clear()
            miner_list.append(miner)

    return miner_list

# number of validators should be less than or equal to the number of nodes in the network
def ePOS(network, blocks):
    block_map = dict()
    for block in blocks:
        block_map[block] = []
 
    for node in network.nodes:
        b = find_best_block(node, blocks)
        if b is not None:
            block_map[b].append(node)
    
    prev = []
    for block in block_map:
        min_w, max_w = network.find_min_max_wealth()
        potential_miners = block_map[block]
        if len(potential_miners) == 0:
            potential_miners = prev
            if len(prev) == 0:
                min_miner = network.find_rand_node()
                min_miner.update(network.block_reward, np.random.randint(6,12))
                continue
        
        potential_miners.sort(key=lambda m: (m.blocks_mined, -m.wealth))
        min_miner = potential_miners[0]

        min_miner.update(network.block_reward, np.random.randint(6,12))
        
        if len(block_map[block]) != 0:
            potential_miners.remove(min_miner)
            for m in potential_miners:
                prev.append(m)
        else:
            prev.remove(min_miner)
            

        



