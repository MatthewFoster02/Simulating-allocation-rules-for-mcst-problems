from graph.node import Node

class Edge:
    def __init__(self, start_node:Node, end_node:Node, cost:int):
        self.start_node = start_node
        self.end_node = end_node
        self.cost = cost

    def set_start_node(self, start_node:Node):
        self.start_node = start_node

    def set_end_node(self, end_node:Node):
        self.end_node = end_node

    def set_cost(self, cost:int):
        self.cost = cost
    
    def get_start_node(self):
        return self.start_node
    
    def get_end_node(self):
        return self.end_node
    
    def get_cost(self):
        return self.cost
    
    def is_same_edge_excluding_cost(self, other_edge:'Edge'):
        return  self.start_node.get_label() == other_edge.get_start_node().get_label() and \
                self.end_node.get_label() == other_edge.get_end_node().get_label()
    
    def to_string(self):
        return f"Node {self.start_node.get_label()} is connected to {self.end_node.get_label()} with cost of {self.cost}"
