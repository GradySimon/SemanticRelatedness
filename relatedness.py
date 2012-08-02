import networkx as nx

class Semantic_Network:
    """ A Semantic_Network captures all of the information about the inter-relatedness of concepts (words) in a particular space (space used non-technically here). It contains a set of words, and a set of connections between those words. A connection is fully specified by the two words it connects, and the strength it connects. Behind the scenes, a Semantic_Network is a flow-network graph, with the words serving as nodes, the connections serving as flow-paths, and the strengths of those connections serving as the capacity of each of those flow-paths. Relatedness is calculated as a max-flow calculation with some modifications (see the doc string for calc_relatedness). 
    """
    def __init__(self, path=None):
        """ Returns a Semantic_Network. If path is specifed, the returned Semantic_Network will contain data from the edgelist file specified. If path is not specified, the returned Semantic_Network will be empty.
        """
        if path is not None:
            self.graph = nx.read_edgelist(path, comments='^', delimiter="<->", data=[("capacity", float,)])
        else:
            self.graph = nx.Graph()

    def add_entity(self, entity):
        """ Adds the entity to the Semantic_Network. Note that it is possible to add a connection to the Semantic_Network before adding both or either of the entities involved. Doing so will effectively add both entities to the network.
        """
        self.graph.add_node(entity)

    def add_entities(self, entities):
        """ Adds all of the entities in the iterable entities to the Semantic_Network
        """
        for entity in entities:
            self.add_entity(entity)

    def connect(self, first_entity, second_entity, strength):
        """ Connects first_entity to second_entity, with a strength of strength.
        """
        self.graph.add_edge(first_entity, second_entity, capacity=strength)

    def add_connections(self, connections):
        """ Adds every connection from iterable connections to the Semantic_Network.
        """
        for connection in connections:
            self.connect(*connection)

    def remove_entity(self, entity):
        """ Removes the entity from the Semantic_Network. This also removes all connections involving this entity.
        """
        self.graph.remove_node(entity)

    def remove_connection(self, first_entity, second_entity):
        """ Removes the connection between first_entity and second_entity. This does not remove the two entities from the Semantic_Network.
        """
        self.graph.remove_edge(first_entity, second_entity)

    def calc_relatedness(self, first_entity, second_entity):
        """ Returns the relatedness of the two entities. Relatedness is a value that corresponds to how semantically connected two words are. Note that this is not necessarily a measure of how similar two words are to each other in meaning. To illustrate the distinction between these two ideas, consider that "cat" and "mouse", depending on the dataset, might be as related as "mouse" and "rat", even though "mouse" and "rat" are much more similar to each other than "cat" and "mouse" are.

        Relatedness is calculated by first constructing what is deemed a "decaying subgraph" centered on the two words. This is constructed starting with a graph that is comprised of only the two words. Then, all of the edges connected to those two words are added to the graph. The strength of those connections is equal to the strength of those connections in the Semantic_Network. Then, all of the neightboring edges to the neighbors of the initial words are added, but this time, each connection has only half of the strength it does in the greater Semantic_Network. This is repeated to contain edges 3 steps away from the two central words. Each level out from the central words, the strength of the connections in the decaying subgraph are halved again, thus, the connections at the third level away from the central words have 25% of the strength that they do in the greater Semantic_Network.

        Once this decaying subgraph is constructed, the max flow between the two words, using strengths of connections as path capacitites, is calculated between the two words. The max flow is returned as the relatedness of the two entities. 
        """
        subgraph = get_decaying_subgraph(self.graph, 
                                        [first_entity, second_entity])
        return nx.max_flow(subgraph, first_entity, second_entity)

    def get_strength_dict(self):
        return get_capacity_dict(self.graph)

    def save_to_file(self, path):
        """ Saves an edgelist representation of this Semantic_Network to the file specified by path. This edgelist can later be read to reconstruct this Semantic_Network.
        """
        nx.write_edgelist(self.graph, path, data=["capacity"], delimiter="<->")

    

def get_decaying_subgraph(graph, start_nodes, max_hops=3, decay_rate=0.5):
    """ Constructs a decaying subgraph centered on all of the nodes in iterable start_nodes.
    """
    subgraph = nx.Graph()
    subgraph.add_nodes_from(start_nodes)
    seen_node_set = set()
    hop_node_set = set(start_nodes)
    next_hop_set = set()
    for hop in range(max_hops):
        decay_multiplier = decay_rate ** hop
        for node in hop_node_set:
            for neighbor in graph.neighbors(node):
                if subgraph.has_edge(node, neighbor):
                    continue
                next_hop_set.add(neighbor)
                # print "Node: %s <-> Neighbor: %s" % (node, neighbor)
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

