import numpy as np
from time import sleep
from copy import deepcopy

'''
extended PoS
https://ieeexplore.ieee.org/abstract/document/9312484


'''

# find the block with the greatest transaction
# fee that does not exceed the node's current wealth
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

# number of validators should be less than or equal to the number of nodes in the network
def ePOS(network, blocks):

    # setup potential miners for each block
    block_map = dict()
    for block in blocks:
        block_map[block] = []
 
    # find best block for each node
    for node in network.nodes:
        b = find_best_block(node, blocks)
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
                min_miner = network.find_rand_node()
                min_miner.update(network.block_reward, np.random.randint(6,12))
                continue
        
        # sort list of potential miners based on least blocks mined and then highest wealth
        potential_miners.sort(key=lambda m: (m.blocks_mined, -m.wealth))

        # find miner and give reward (assuming honest validation)
        min_miner = potential_miners[0]
        min_miner.update(network.block_reward, np.random.randint(6,12))
        
        # remove selected miner from potential list for future blocks
        if len(block_map[block]) != 0:
            potential_miners.remove(min_miner)
            for m in potential_miners:
                prev.append(m)
        else:
            prev.remove(min_miner)
            

        



