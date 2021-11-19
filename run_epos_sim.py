import numpy as np

'''
run simulator
'''
from ePOS_Model import *
from ePOS import *

def run_sim(iters=30000):
    #make a storage list 
    net = network(1000)

    centralization_overtime = []

    for k in range(iters):
        blocks = net.create_blocks()
        ePOS(net, blocks)
        if k % 100 == 0:
            centralization_val = net.calc_centralization()
            centralization_overtime.append(centralization_val)
            print(centralization_val)

    print(centralization_overtime)

if __name__=="__main__":
    run_sim()