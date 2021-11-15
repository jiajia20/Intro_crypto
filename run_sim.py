'''
run simulator
'''
from pPOS_Model import *
from pPOS import *

def take_wealth(elem):
    return elem.wealth

def run_sim(iters=10):
    #make a storage list 
    net = network(100, "normal")

    centralization_overtime = []
    for k in range(iters):
        pPOS(net, 20)
        centralization_val = net.calc_centralization()
        centralization_overtime.append(centralization_val)

    net.nodes.sort(key=take_wealth)
    for j in range(100):
        print(net.nodes[j].wealth)
    return centralization_overtime

if __name__=="__main__":
    run_sim()