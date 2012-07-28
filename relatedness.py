import networkx as nx

class Semantic_Network:

    def __init__(self, path=None):
        if path is not None:
            self.graph = nx.read_edgelist(path)
        else:
            self.graph = nx.Graph()

    def add_entity(self, entity):
        self.graph.add_node(entity)

    def add_entities(self, entities):
        for entity in entities:
            self.add_entity(entity)

    def connect(self, first_entity, second_entity, strength):
        self.graph.add_edge(first_entity, second_entity, capacity=strength)

    def add_connections(self, connections):
        for connection in connections:
            self.connect(*connection)

    def remove_entity(self, entity):
        self.graph.remove_node(entity)

    def remove_connection(self, first_entity, second_entity):
        self.graph.remove_edge(first_entity, second_entity)

    def calc_relatedness(self, first_entity, second_entity):
        subgraph = get_decaying_subgraph(self.graph, 
                                        [first_entity, second_entity])
        return nx.max_flow(subgraph, first_entity, second_entity)

    def get_strength_dict(self):
        return get_capacity_dict(self.graph)

    def save_to_file(self, path):
        nx.write_edgelist(self.graph, path, data=True)

    

def get_decaying_subgraph(graph, start_nodes, max_hops=3, decay_rate=0.5):
    subgraph = nx.Graph()
    subgraph.add_nodes_from(start_nodes)
    seen_node_set = set()
    hop_node_set = set(start_nodes)
    next_hop_set = set()
    for hop in range(max_hops):
        decay_multiplier = decay_rate ** hop
        # active_set = [node for hop_node_set if node not in seen_node_set]
        for node in hop_node_set:
            for neighbor in graph.neighbors(node):
                if subgraph.has_edge(node, neighbor):
                    continue
                next_hop_set.add(neighbor)
                decayed_capacity = (decay_multiplier * 
                                    graph[node][neighbor]['capacity']) 
                subgraph.add_edge(node, neighbor, capacity=decayed_capacity) 
            seen_node_set.add(node)
        hop_node_set = next_hop_set - seen_node_set
        next_hop_set.clear()
    return subgraph
                
def get_capacity_dict(graph):
    capacity_dict = dict()
    for edge in graph.edges():
        capacity_dict[edge] = graph.get_edge_data(*edge)['capacity']
    return capacity_dict

