'''
run simulator
'''
from Models import *
from protocol import *
import csv

def run_sim(iters=10001):
    net = network(10000)
    protocol = ePOS(net)

    centralization_overtime = []
    for k in range(iters):
        protocol.validate_block(5)
        if (k%100 == 0):
            centralization_val = net.gini_coefficient()
            print(k, "= ", centralization_val)
            centralization_overtime.append((k,centralization_val))

            if (False):
                nodes_g = [x.greed for x in net.nodes]
                avg_g = sum(nodes_g) / net.num_nodes
                max_g = max(nodes_g)
                min_g = min(nodes_g)
                nodes_w = [x.wealth for x in net.nodes]
                avg_w = sum(nodes_w) / net.num_nodes
                max_w = max(nodes_w)
                min_w = min(nodes_w)
                print(f"    AVERAGE G: {avg_g}")
                print(f"    MAX G: {max_g}")
                print(f"    MIN G: {min_g}")
                print(f"    AVERAGE W: {avg_w}")
                print(f"    MAX W: {max_w}")
                print(f"    MIN W: {min_w}")

    with open('ePOS_results.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['iteration','gini coefficient'])
        for row in centralization_overtime:
            csv_out.writerow(row)


if __name__=="__main__":
    run_sim()