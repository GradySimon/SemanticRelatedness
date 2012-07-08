import networkx as nx

class Semantic_Network:

    def __init__(self):
        self.graph = nx.Graph()

    def add_entity(self, entity):
        self.graph.add_node(entity)

    def connect(self, first_entity, second_entity, strength):
        edge = (first_entity, second_entity, {'capacity':strength})
        self.graph.add_edge(*edge)

    def remove_entity(self, entity):
        self.graph.remove_node(entity)

    def remove_connection(self, first_entity, second_entity):
        self.graph.remove_edge(first_entity, second_entity)

    # def calc_relatedness(self, first_entity, second_entity):
        
