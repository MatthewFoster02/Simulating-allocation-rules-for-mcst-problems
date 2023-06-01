import random
from graph.node import Node
from graph.edge import Edge

class Graph:
    def __init__(self, edges:list[Edge]=None, sources:list[Node]=None, players:list[Node]=None):
        self.edges = edges
        self.sources = sources
        self.players = players
    
    def set_edges(self, edges:list[Edge]):
        self.edges = edges

    def get_edges(self):
        return self.edges
    
    def set_sources(self, sources:list[Node]):
        self.sources = sources

    def get_sources(self):
        return self.sources
    
    def set_players(self, players:list[Node]):
        self.players = players

    def get_players(self):
        return self.players
    
    def generate_random_graph(self, num_sources:int=2, num_players=3):
        self.sources:list = self.generate_sources(num_sources)
        self.players:list = self.generate_players(num_players)
        nodes = self.sources + self.players
        self.edges = self.generate_edges(nodes)
    
    def generate_sources(self, num_sources:int):
        sources = []
        for i in range(num_sources):
            sources.append(Node(type='source', label=chr(i + 97)))
        return sources
    
    def generate_players(self, num_players:int):
        players = []
        for i in range(num_players):
            players.append(Node(label=i+1))
        return players
    
    def generate_edges(self, nodes:list[Node]):
        edges = []
        for i in range(len(nodes)-1):
            for j in range(i+1, len(nodes)):
                edges.append(Edge(start_node=nodes[i], end_node=nodes[j], cost=random.randint(1, 20)))
        return edges
    
    def check_path_between_2_nodes(self, node_u_label, node_v_label):
        visited = set()
        return self.depthFirstSearch(node_u_label, node_v_label, visited)
    
    def depthFirstSearch(self, current_node, end_node, visited:set):
        if current_node == end_node:
            return True
        
        visited.add(current_node)

        for edge in self.edges:
            # Complicated way of checking whether an edge has an endpoint which is the current node and the other end point has not yet been visited
            if edge.start_node.get_label() == current_node and edge.end_node.get_label() not in visited:
                if self.depthFirstSearch(edge.end_node.get_label(), end_node, visited):
                    return True
            if edge.end_node.get_label() == current_node and edge.start_node.get_label() not in visited:
                if self.depthFirstSearch(edge.start_node.get_label(), end_node, visited):
                    return True
        
        return False
    
    def to_string(self):
        return_string = ''
        for edge in self.edges:
            return_string += f'{edge.to_string()}\n'
        return return_string
