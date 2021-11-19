import random as rd

"""
pPOS 
https://www.algorand.com/technology/white-papers
"""

# number of validators should be less than or equal to the number of nodes in the network
def pPOS(network, num_validators):

    # find number of nodes in network
    node_num = network.number_of_nodes()

    # chance of getting selected should be proportional to stake
    players = []
    for i in range(node_num):
        player = network.nodes[i]
        for i in range(int(player.wealth)):
            players.append(player)
    rd.shuffle(players)
    
    # find validators
    for i in range(num_validators):
        winner = players[0]

        # assume honest validating
        
        # simulate giving reward (need to discuss)
        transaction_reward = rd.randint(1,4)
        winner.update(network.block_reward, transaction_reward)

        # validator can only be chosen once per epoch
        players = list(filter(lambda a: a.id != winner.id, players))