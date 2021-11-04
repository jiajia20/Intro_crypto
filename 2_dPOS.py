'''
Delegated PoS

Mechanism 1 is a version of delegated PoS that resemles the TheGraph's incentive layer.
Service providers are devided into two group: delegators and indexer.
Delegators delegate stake and earn a portion of reward from indexers.

Indexer provide service and they are elected in a permissionless fashion. 
Indexers gets block reward, divide among themselves and their delegators.

While in practice the ratio of spliting block rewards are decide dynamically by the indexer, here we assume
the rewards are splot 50-50

the Graph visualize the deletation relationships.


https://github.com/EOSIO/Documentation/blob/master/TechnicalWhitePaper.md#consensus-algorithm-bft-dpos
'''