import copy

from graph.graph import Graph
from graph.edge import Edge

class RegularReduce:
    def __init__(self, graph:Graph=None, mcst_edges:list[Edge]=None):
        self.graph = graph
        self.mcst_edges = mcst_edges
    
    def reduce_graph(self) -> Graph:
        # Get edges not in mcst
        # For each edge above -> check path between two endpoints
        #       - Update edge cost to max weight on path from start node to source node (get the max weight on path)
        # Create new graph with original mcst_edge unchanged, and the edges with reduced weight.

        edges_not_in_mcst = self.get_edges_not_in_mcst()
        for edge in edges_not_in_mcst:
            path_in_mcst = self.find_path_in_mcst(edge)
            max_cost_on_path = self.get_max_cost_on_path(path_in_mcst)
            edge.set_cost(max_cost_on_path)
        
        new_edges = []
        for edge in self.mcst_edges:
            new_edges.append(edge)
        for edge in edges_not_in_mcst:
            new_edges.append(edge)
        return Graph(edges=new_edges, sources=self.graph.get_sources(), players=self.graph.get_players())
    
    # TESTED
    def get_edges_not_in_mcst(self) -> list[Edge]:
        mcst_edges_str = []
        for edge in self.mcst_edges:
            mcst_edges_str.append(edge.to_string())
        
        edges_not_in_mcst = []
        for edge in self.graph.get_edges():
            if edge.to_string() not in mcst_edges_str:
                edges_not_in_mcst.append(edge)
        return copy.deepcopy(edges_not_in_mcst)

    # TESTED
    def find_path_in_mcst(self, edge:Edge):
        start_label = edge.get_start_node().get_label()
        end_label = edge.get_end_node().get_label()
        return self.get_path(start_label=start_label, end_label=end_label)

    # TESTED
    def get_max_cost_on_path(self, path:list[Edge]):
        max_cost = -1 # All edges have cost > 0 so -1 is safe lowerbound
        for edge in path:
            if edge.get_cost() > max_cost:
                max_cost = edge.get_cost()
        return max_cost
    
    # TESTED
    def get_path(self, start_label, end_label):
        self.current_path = []
        visited = set()
        if self.depthFirstSearch(current_node=start_label, end_node=end_label, visited=visited):
            return copy.deepcopy(self.current_path)

    def depthFirstSearch(self, current_node, end_node, visited:set):
        if current_node == end_node:
            return True
        
        visited.add(current_node)

        for edge in self.mcst_edges:
            # Complicated way of checking whether an edge has an endpoint which is the current node and the other end point has not yet been visited
            if edge.start_node.get_label() == current_node and edge.end_node.get_label() not in visited:
                if self.depthFirstSearch(edge.end_node.get_label(), end_node, visited):
                    self.current_path.append(edge)
                    return True
            if edge.end_node.get_label() == current_node and edge.start_node.get_label() not in visited:
                if self.depthFirstSearch(edge.start_node.get_label(), end_node, visited):
                    self.current_path.append(edge)
                    return True
        
        return False
