Read Me

## Project Abstract
Centralization is an issue that has begun to arise in major cryptocurrency solutions
as the creation of mining pools, cost of mining hardware, and hoarding of currency
has increased overtime. In this paper, we are going to determine whether Proof-
of-Stake cryptocurrencies tend to become centralized over time or not. To do so,
we used agent-based modeling to run simulations of various con gurations of Proof-
of-Stake systems, such as Delegated Proof-of-Stake, Extended Proof-of-Stake, and
Pure Proof-of-Stake to observe the collection of wealth over time. Finally, we tried
to  nd an improvement to the proof-of-stake system with our own design, called
Raffle Proof-of-Stake.

## About POS
In Proof of Stake is a variation of consensus algorithms of distributed systems. 
The goal is to 
1) maintain a shared record with the presence of malicious participants - BFT
2) maintain transaction record , keep it updating without the need of a global clock.
3) use incentive systems i.e. reward service providers with tokens of montary values, to create a ledger that countonues maintain a shared record despite certain percentage of malicious/adversarial participants. 

## Scope & Limiation
In this paper:
### Consensus
We assume the participaion are permissionless. Since clearly a permissioned blockchain can be replaced with a distributed network run by a centralized service provider and it makes no sense to take about decentralization at that point. 

We also assume that some of the participants are honest and others are rationally selfish (responde to ecnomic incentive). The vulunerability of the systems resides on certain percentage of the particpants being honest (more specifically, percentage of the stake hold by honest participants). We argue that while majority attack (holding 51% of decision power)can happen, when it actually happens, the rest of the network can fork the system so that the majority attacker holds no tokens [source](https://cointelegraph.com/news/hive-hard-fork-is-successful-steem-crashes-back-to-earth).

We focus soly on the economic layer (i.e. how stakes change over time according to the stake collection and reward mechanism) while leave the excat implementation of the consensus forming mechanism out of the scope of discussion.


### Wealth
We assume that the system is relatively closed, i.e. we do not consider the wealth centralization caused by a whale come in with large sum of cash and take over the stake by buying crypto with many us dollars.

While network resilience also lies in the geographical discentrlization of server and service providers. We leave the discussion of geographical decentralization out of the scope. Possible implication for geographical decentralization are briefly discussed but not extensively investigated. 

We focus on what design of staking participation and reward will increase wealth decentralization (reduce the likelyhood of rich get richer) without causing damage to the security to our best knowledge. 

## Models
### miners/service providers
selected miner for a transaction $\subset$ all miners $\subset$ all account holders
Among those participants, a percentage are honest, others are rationally selfish.
Miners are selected through a variation of staking process to mine the next block. The staking process freeze the stake and the reward process allocate rewards back to the miners (and/or their supporters). participants accumulate wealth through this process.

### rewards 
Rewads are distributed through two mainsource: transaction fees and block reward - both are given to the miners (and/or their supporters).
selection of how much stake is needed to participate, who gets the reward, and how much reward is given to who creates the change of the distribution of wealth. 

### mining, transaction and attacks
Mining happens as follows:
Many transactions make a block,
Many blocks make an epoch
Epochs make up the chain.

Miner are rewarded with the transaction fee and potentially block reward associated with a block. Each variation of POS produce different implimentation of mining, transaction and also vlunerable for different attacks. 


## Evaluatoin
We focus our evaluation on decentralization of wealth as a result of the mining reward layer. We also inviestigate the impact of POS design on security.

### Decentralization
Decentralization are measured in four matric. 
- 
- 

### Security 
We test limitation:

## Goal
- 


## Modeling decentralization and decurity of POS Consensus Algorithms

- the numbered file are implementation of different POS mechanism
- the models are 
- security.py analyze common security 
- decentralization_analytics.py analyze 4 different matric of wealth decentralization
- the notebook are used for visualizations

Our framework runs as follows:
- each 


## Limitation
- sophisticated attacks such as grinding attacks are not discussed in the security analysis. It's possible that new design can be gamed with well-targetted attacks
- We only discussed wealth centralization, more specifically, the nartually emerging pattern of rich get richer and eventually take over the network.



## Notes
### Terms to define
- miners
- economic layer/incentive layer
- attacks we evaluate 


## Work/ ToDO
- how staking happens step by step
