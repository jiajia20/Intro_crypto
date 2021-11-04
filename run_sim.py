'''
delegated PoS
'''


def run_sim(network, di, iters=100, mvy = 0, mry = 0):
    #make a storage list 
    mood_overtime = []
    for k in range(iters):
        mood_value = play(network, di, mvy, mry)
        mood_overtime.append(mean(mood_value))
        
    return mood_overtime   