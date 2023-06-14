import copy

from graph.graph import Graph
from graph.edge import Edge

class PathRule:
    def __init__(self, graph:Graph=None, mcst_edges:list[Edge]=None, source_a_set:set=None, source_b_set:set=None):
        self.graph = graph
        self.mcst_edges = mcst_edges
        self.source_a_set = source_a_set
        self.source_b_set = source_b_set

        if graph is not None:
            self.cost_allocation = [0] * len(self.graph.get_players())
    
    # TESTED
    def run_rule(self):
        # SET UP
        self.get_individual_player_costs()
        self.get_path_player_costs()

        while self.does_one_player_have_edges():
            no_player_to_pay = self.check_for_player_who_can_pay()
            if no_player_to_pay:
                return False
    
    # TESTED
    def does_one_player_have_edges(self):
        for _, players_edges in self.player_path_edges.items():
            if len(players_edges) > 0:
                return True
        return False

    # TESTED
    def get_individual_player_costs(self):
        self.individual_cost = {}
        source_player_edges:list[Edge] = []
        for player in self.graph.get_players():
            self.individual_cost[str(player.get_label())] = 0
            if player.get_label() in self.source_a_set:
                source_player_edges.append(self.getEdgeBetweenPlayerAndSource(player_label=player.get_label(), source_label='a'))
            elif player.get_label() in self.source_b_set:
                source_player_edges.append(self.getEdgeBetweenPlayerAndSource(player_label=player.get_label(), source_label='b'))

        for edge in source_player_edges:
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if type(start_label) == int:
                self.individual_cost[str(start_label)] = edge.get_cost()
            else:
                self.individual_cost[str(end_label)] = edge.get_cost()

    def getEdgeBetweenPlayerAndSource(self, player_label:int, source_label:str) -> Edge:
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if start_label == player_label and end_label == source_label:
                return edge
            if start_label == source_label and end_label == player_label:
                return edge
    
    # TESTED
    def get_path_player_costs(self):
        self.player_path_cost = {}
        self.player_path_edges = {}
        for player in self.graph.get_players():
            wanted_source = self.get_wanted_source(player.get_label())
            edges_between_player_and_source = self.get_path(player.get_label(), wanted_source)
            self.player_path_cost[str(player.get_label())] = self.get_path_cost(edges_between_player_and_source)
            self.player_path_edges[str(player.get_label())] = edges_between_player_and_source

    # TESTED
    def get_wanted_source(self, player_label:int):
        if player_label in self.source_a_set:
            return 'a'
        
        if player_label in self.source_b_set:
            return 'b'

    # TESTED
    def get_path(self, player_label:int, source_label:str):
        self.current_path = []
        visited = set()
        if self.depthFirstSearch(player_label, end_node=source_label, visited=visited):
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

    # TESTED
    def get_path_cost(self, edges_in_path:list[Edge]):
        path_cost = 0
        for edge in edges_in_path:
            path_cost += edge.get_cost()
        return path_cost

    # TESTED
    def check_for_player_who_can_pay(self):
        no_player = True
        for player in self.graph.get_players():
            players_path_cost = self.player_path_cost[str(player.get_label())]
            if players_path_cost > 0 and players_path_cost <= self.individual_cost[str(player.get_label())]:
                no_player = False
                self.player_pays_for_edges(player.get_label())
                self.player_remove_edges(player.get_label())
        
        return no_player

    # TESTED
    def player_pays_for_edges(self, player_label:int):
        cost_to_pay = self.get_path_cost(self.player_path_edges[str(player_label)])
        self.cost_allocation[player_label-1] = cost_to_pay
    
    # TESTED
    def player_remove_edges(self, player_label:int):
        for edge in self.player_path_edges[str(player_label)]:
            self.remove_edge_from_all(edge, player_label)
        
        self.player_path_edges[str(player_label)] = []
        self.update_player_path_costs()

    # TESTED
    def remove_edge_from_all(self, edge:Edge, player_label:int):
        edge_as_string = edge.to_string()

        for player, players_edges in self.player_path_edges.items():
            if player == str(player_label):
                continue
            for edge_in_path in players_edges:
                if edge_in_path.to_string() == edge_as_string:
                    players_edges.remove(edge_in_path)

    # TESTED
    def update_player_path_costs(self):
        for player in self.graph.get_players():
            self.player_path_cost[str(player.get_label())] = self.get_path_cost(self.player_path_edges[str(player.get_label())])

    # BOILERPLATE
    def get_individual_cost(self):
        return self.individual_cost
    
    def set_individual_cost(self, individual_cost):
        self.individual_cost = individual_cost
    
    def get_player_path_cost(self):
        return self.player_path_cost
    
    def set_player_path_cost(self, player_path_cost):
        self.player_path_cost = player_path_cost
    
    def get_player_path_edges(self):
        return self.player_path_edges
    
    def set_player_path_edges(self, player_path_edges):
        self.player_path_edges = player_path_edges

    def get_cost_allocation(self):
        return self.cost_allocation
