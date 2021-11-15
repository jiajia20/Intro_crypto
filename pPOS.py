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
        players.append((i, player)*int(player.wealth))
    rd.shuffle(players)
    
    # find validators
    for i in range(num_validators):
        winner = players[0]

        # assume honest validating
        
        # simulate giving reward (need to discuss)
        reward = rd.randint(1,8)
        winner[1].update(reward)

        # validator can only be chosen once per epoch
        players = list(filter(lambda a: a[0] != winner[0], players))