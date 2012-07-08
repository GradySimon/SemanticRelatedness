import networkx as nx

class Semantic_Network:

    def __init__(self):
        self.graph = nx.Graph()

    def add_entity(self, entity):
        self.graph.add_node(entity)

    def connect(self, first_entity, second_entity, strength):
        self.graph.add_edge(first_entity, second_entity, capacity=strength)

    def remove_entity(self, entity):
        self.graph.remove_node(entity)

    def remove_connection(self, first_entity, second_entity):
        self.graph.remove_edge(first_entity, second_entity)

    def calc_relatedness(self, first_entity, second_entity):
        subgraph = get_decaying_subgraph(self.graph, [first_entity, second_entity])
        # calculate max flow from first_entity to second_entity        
        return max_flow(subgraph, first_entity, second_entity)

def get_decaying_subgraph(graph, start_nodes, max_hops=3, decay_rate=0.5):
    subgraph = nx.Graph()
    subgraph.add_node(start_node)
    seen_node_set = set()
    hop_node_set = set(start_nodes)
    next_hop_set = set()
    decay_multiplier = 1 - decay_rate
    for hop in range(max_hops):
        decay_multiplier **= hop 
        for node in hop_node_set if node not in seen_node_set:
            for neighbor in node.neighbors()
                if subgraph.has_edge(node, neighbor):
                    continue
                next_hop_set.add(neighbor)
                decayed_capacity = decay_multiplier * graph[node][neighbor]['capacity'] 
                subgraph.add_edge(node, neighbor, capacity=decayed_capacity) 
            seen_node_set.add(node)
        hop_node_set = next_hop_set
        next_hop_set.clear()
    return subgraph
                
