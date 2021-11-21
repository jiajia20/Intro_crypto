import numpy as np
import csv

'''
run simulator
'''
from ePOS_Model import *
from ePOS import *

def run_sim(iters=1000):
    #make a storage list 
    net = network(10000)

    centralization_overtime = []

    for k in range(iters):
        blocks = net.create_blocks()
        ePOS(net, blocks)
        if k % 10 == 0:
            centralization_val = net.calc_centralization()
            centralization_overtime.append((k,centralization_val))

    with open('ePOS_results.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['iteration','gini coefficient'])
        for row in centralization_overtime:
            csv_out.writerow(row)


if __name__=="__main__":
    run_sim()