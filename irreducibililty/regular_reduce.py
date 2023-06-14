from graph.graph import Graph
from graph.edge import Edge

class RegularReduce:
    def __init__(self, graph:Graph=None, mcst_edges:list[Edge]=None):
        self.graph = graph
        self.mcst_edges = mcst_edges
    
    def reduce_graph(self):
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
            new_edges.append(edges_not_in_mcst)
        return Graph(edges=new_edges, sources=self.graph.get_sources(), players=self.graph.get_players())
    
    def get_edges_not_in_mcst(self) -> list[Edge]:
        mcst_edges_str = []
        for edge in self.mcst_edges:
            mcst_edges_str.append(edge.to_string())
        
        edges_not_in_mcst = []
        for edge in self.graph.get_edges():
            if edge.to_string() not in mcst_edges_str:
                edges_not_in_mcst.append(edge)
        return edges_not_in_mcst

    def find_path_in_mcst(self, edge:Edge):
        pass

    # TESTED
    def get_max_cost_on_path(self, path:list[Edge]):
        max_cost = -1 # All edges have cost > 0 so -1 is safe lowerbound
        for edge in path:
            if edge.get_cost() > max_cost:
                max_cost = edge.get_cost()
        return max_cost

    # BOILERPLATE