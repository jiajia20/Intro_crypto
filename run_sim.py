'''
run simulator
'''
from Models import *
from protocol import *
import csv

def run_sim(iters=10001):
    net = network(10000)
    protocol = dPOS_GT(net)

    centralization_overtime = []
    for k in range(iters):
        protocol.validate_block(5)
        if (k%100 == 0):
            centralization_val = net.gini_coefficient()
            print(k, "= ", centralization_val)
            centralization_overtime.append((k,centralization_val))

    with open('dPOS_GT_real_results.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['iteration','gini coefficient'])
        for row in centralization_overtime:
            csv_out.writerow(row)


if __name__=="__main__":
    run_sim()