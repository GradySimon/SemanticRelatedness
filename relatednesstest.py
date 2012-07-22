import matplotlib.pyplot as plt
import networkx as nx
from relatedness import *

dog_entities = ["dog", "cat", "horse", "saddle", "rider", "mouse", "cheese",
                "churning", "milk", "cow", "human", "race", "gambling"]
dog_connections = [("dog", "cat", 50), 
                    ("dog", "horse", 10),
                    ("horse", "saddle", 60),
                    ("horse", "rider", 30),
                    ("rider", "saddle", 40),
                    ("horse", "race", 30),
                    ("rider", "race", 35),
                    ("dog", "race", 20),
                    ("cat", "mouse", 50),
                    ("race", "gambling", 40),
                    ("mouse", "cheese", 50),
                    ("cheese", "milk", 60),
                    ("milk", "cow", 60),
                    ("cheese", "cow", 30),
                    ("rider", "human", 50),
                    ("milk", "churning", 20),
                    ("human", "gambling", 30)]

def get_test_network1():
    network = Semantic_Network()
    network.add_entities(dog_entities)
    network.add_connections(dog_connections)
    return network

def draw_network(network, location=None):
    graph = network.graph
    draw_graph(graph, location)

def draw_graph(graph, location=None):
    positions = nx.spring_layout(graph)
    labels = get_capacity_dict(graph)
    plt.clf()
    nx.draw(graph, positions)
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=labels)
    if location is None:
        plt.ion()
        plt.show()
    else:
        plt.savefig(location)

# if __name__=="__main__":
    
