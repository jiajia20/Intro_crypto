'''
Priority Selection (OG) PoS
Mechanism 1 is random selection PoS.

A random portion of network (0-100%) can choose to stake.
Their chance to be selected pertain to the amount they stake (assume they stake everything).
'''
import random as rd
def mech1(network, directory):  

# 

    #play game
    ##shuffule
    node_num = network.number_of_nodes()
    index = list(range(node_num))
    rd.shuffle(index)
    
    for i in index:
        #didn't shuffle neighbors but figured won't need to shuffle twice??
        neighbors = [n for n in network.neighbors(i)]
        player = directory.get(i) #return player agent
        for j in neighbors:
            player.game(directory.get(j)) #play a interaction game and update accordingly
         
    # each network only update their mood with noise and regression ONCE after everyone done playing
    if(mry == 1):
        for i in index:
            player = directory.get(i) 
            player.mood_regression()
            
    if(mvy == 1):
        for i in index:
            player = directory.get(i) 
            player.mood_vary() 

            
    #record the mood
    mood_value = []
    for i in list(directory.values()):
        mood_value.append(i.mood)
         
    return  mood_value