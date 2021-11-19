'''
run simulator
'''
from pPOS_Model import *
from pPOS import *

def run_sim(iters=1000):
    #make a storage list 
    net = network(1000)

    centralization_overtime = []
    for k in range(iters):
        num_validators = rd.randint(1, 4)
        pPOS(net, num_validators)
        if k % 100 == 0:
            centralization_val = net.calc_centralization()
            centralization_overtime.append(centralization_val)
            print(centralization_val)


if __name__=="__main__":
    run_sim()