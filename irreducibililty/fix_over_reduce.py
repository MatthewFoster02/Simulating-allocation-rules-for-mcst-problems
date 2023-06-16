import copy

from cooperative_functions.cooperative_gt import CoopMethods
from graph.graph import Graph
from graph.edge import Edge

class FixOverReduce:
    def __init__(self, reduced_graph:Graph=None,
                 mcst_edges:list[Edge]=None,
                 original_graph:Graph=None,
                 original_coalitions:dict=None,
                 source_a_set:set=None,
                 source_b_set:set=None):
        self.reduced_graph = reduced_graph
        self.mcst_edges = mcst_edges
        self.original_graph = original_graph
        self.original_coalitions = original_coalitions
        self.source_a_set = source_a_set
        self.source_b_set = source_b_set
    
    def fix_over_reduce(self) -> Graph:
        # Take in the reduced graph and original graph and all others as before
        # Loop through every edge and decrease by one until
        #   a) The cost of the edge is equal to its cost in the reduced graph.
        #   b) Reducing the edge anymore results in different value for grand coalition (2 component optimal solution)

        for edge in self.original_graph.get_edges():
            if self.no_further_reduce(edge):
                continue

            edge.reduce_cost() # Increase cost

        return self.original_graph

        # Find cost in mcst for each player to connect to its wanted source
        # Keep the minimum cost for each source, a and b
        # Check edges in Na and Nb, make sure all are at least this cost from above


        # costs = {
        #     'a': 10000,
        #     'b': 10000
        # }
        # for player in self.reduced_graph.get_players():
        #     cost_to_connect_to_source = self.find_cost_in_mcst_to_source(player.get_label())
        #     if player.get_label() in self.source_a_set and cost_to_connect_to_source < costs['a']:
        #         costs['a'] = cost_to_connect_to_source
            
        #     if player.get_label() in self.source_b_set and cost_to_connect_to_source < costs['b']:
        #         costs['b'] = cost_to_connect_to_source

        # edges_a = self.get_edges_between_players_and_source('a')
        # edges_b = self.get_edges_between_players_and_source('b')
        # for edge in edges_a:
        #     if self.edge_in_mcst(edge):
        #         continue
        #     if edge.get_cost() < costs['a']:
        #         edge.set_cost(costs['a'])
        # for edge in edges_b:
        #     if self.edge_in_mcst(edge):
        #         continue
        #     if edge.get_cost() < costs['b']:
        #         edge.set_cost(costs['b'])
        
        # # Ensure edge costs in reduced graph are updated
        # updated_edges = []
        # for edge in self.reduced_graph.get_edges():
        #     no_edge_added = True
        #     for a_edge in edges_a:
        #         if edge.is_same_edge_excluding_cost(a_edge):
        #             updated_edges.append(a_edge)
        #             no_edge_added = False
        #     for b_edge in edges_b:
        #         if edge.is_same_edge_excluding_cost(b_edge):
        #             updated_edges.append(b_edge)
        #             no_edge_added = False
            
        #     if no_edge_added:
        #         updated_edges.append(edge)
        
        # self.reduced_graph.set_edges(updated_edges)

        # return self.reduced_graph
    



    def no_further_reduce(self, edge:Edge):
        edge_at_lower_bound = self.is_edge_at_lower_bound(edge)
        reducing_edge_changes_grand_coalition = self.does_reducing_change_grand_coalition(edge)
        return edge_at_lower_bound or reducing_edge_changes_grand_coalition
    



    def is_edge_at_lower_bound(self, edge:Edge):
        for reduced_edge in self.reduced_graph.get_edges():
            if edge.is_same_edge_excluding_cost(reduced_edge) and edge.get_cost() == reduced_edge.get_cost():
                return True
        return False
    



    def does_reducing_change_grand_coalition(self, edge:Edge):
        edge.reduce_cost()
        if self.is_over_reduced(graph=self.original_graph):
            edge.increase_cost()
            return True
        edge.increase_cost()
        return False
    
    # TESTED
    def is_over_reduced(self, graph:Graph):
        coop = CoopMethods(graph=graph)
        reduced_coalitions = coop.get_player_coalition_values(source_a_set=self.source_a_set, source_b_set=self.source_b_set)
        key = ''.join(str(i) for i in range(1, len(graph.get_players()) + 1))
        return reduced_coalitions[key] < self.original_coalitions[key]
        
    # TESTED
    def find_cost_in_mcst_to_source(self, player_label:int):
        wanted_source = self.find_wanted_source(player_label)
        path_to_source = self.get_path(player_label, wanted_source)
        cost_of_path = self.get_cost_of_path(path_to_source)
        return cost_of_path
    
    def find_wanted_source(self, player_label:int):
        if player_label in self.source_a_set:
            return 'a'
        
        if player_label in self.source_b_set:
            return 'b'
        
    # TESTED
    def get_cost_of_path(self, path:list[Edge]):
        cost = 0
        for edge in path:
            cost += edge.get_cost()
        return cost
    
    # TESTED
    def get_edges_between_players_and_source(self, source_label:str) -> list[Edge]:
        endpoints = [source_label]
        if source_label == 'a':
            endpoints = endpoints + list(self.source_a_set)

        if source_label == 'b':
            endpoints = endpoints + list(self.source_b_set)
        
        return self.get_all_edges_with_endpoints(endpoints)

    # TESTED
    def get_all_edges_with_endpoints(self, endpoints:list):
        edges_to_return = []
        for edge in self.reduced_graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if start_label in endpoints and end_label in endpoints:
                edges_to_return.append(edge)
        return edges_to_return
    
    # TESTED
    def edge_in_mcst(self, edge:Edge):
        for mcst_edge in self.mcst_edges:
            if mcst_edge.is_same_edge_excluding_cost(edge):
                return True
        return False

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
