import requests
import pandas as pd
import networkx as nx
import numpy as np

def readEdgeList(filename):
    edgeList = pd.read_csv(filename)
    if len(edgeList.columns) != 2:
        print 'Warning: csv contains more than 2 columns'
        return edgeList.iloc[:, :2]
    return edgeList

def degree(edgeList, in_or_out):
    if in_or_out is 'in':
        return edgeList['artist2'].value_counts()
    return edgeList['artist1'].value_counts()

def combineEdgeLists(edgeList1, edgeList2):
    return pd.concat([edgeList1, edgeList2]).drop_duplicates()

def pandasToNetworkX(edgeList):
    records = edgeList.to_records(index=False)
    dg = nx.DiGraph()
    dg.add_edges_from(records)
    return dg

def randomCentralNode(inputDiGraph):
    ec = nx.eigenvector_centrality(inputDiGraph)
    total = sum(ec.values())
    ec_norm = {}
    for k,v in ec.items():
        ec_norm[k] = v / total
    return np.random.choice(ec_norm.keys(), p=ec_norm.values())