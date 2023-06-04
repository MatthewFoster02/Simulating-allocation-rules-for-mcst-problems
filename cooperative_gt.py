import itertools
from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from mcst import MCST

class CoopMethods:
    def __init__(self, graph:Graph):
        self.graph = graph
    
    # TESTED
    def get_player_coalition_values(self, source_a_set:set, source_b_set:set):
        # Single player coalitions
        self.source_a_set = source_a_set
        self.source_b_set = source_b_set
        self.player_labels = []
        self.coalitions = {}
        for player in self.graph.get_players():
            if player.get_label() in source_a_set:
                self.coalitions[str(player.get_label())] = self.getEdgeWithEndpoints(player.get_label(), 'a').get_cost()
            elif player.get_label() in source_b_set:
                self.coalitions[str(player.get_label())] = self.getEdgeWithEndpoints(player.get_label(), 'b').get_cost()
            self.player_labels.append(player.get_label())

        # Multi player coalitions
        self.get_coalitions_with_multiple_players(2)
        
        # All players NEED TO CHECK IF MCST OF FULL is less than/equal to mcst of a sub graphs a/b
        mcst_full_graph = MCST(graph=self.graph)
        _, mcst_full_graph_cost = mcst_full_graph.kruskal()

        graph_a_edges = self.getEdgesBetweenPlayersAndSource(list(source_a_set), 'a')
        graph_b_edges = self.getEdgesBetweenPlayersAndSource(list(source_b_set), 'b')

        graph_a_players = []
        for player_label in source_a_set:
            graph_a_players.append(Node(label=player_label))

        graph_b_players = []
        for player_label in source_b_set:
            graph_b_players.append(Node(label=player_label))
        
        graph_a_mcst = MCST(graph=Graph(graph_a_edges, sources=[Node(type='source', label='a')], players=graph_a_players))
        _, graph_a_mcst_cost = graph_a_mcst.kruskal()

        graph_b_mcst = MCST(graph=Graph(graph_b_edges, sources=[Node(type='source', label='b')], players=graph_b_players))
        _, graph_b_mcst_cost = graph_b_mcst.kruskal()


        if mcst_full_graph_cost <= graph_a_mcst_cost + graph_b_mcst_cost:
            print('mcst less')
            self.coalitions[''.join(map(str, self.player_labels))] = mcst_full_graph_cost
        else:
            print('mcst more')
            self.coalitions[''.join(map(str, self.player_labels))] = graph_a_mcst_cost + graph_b_mcst_cost

        return self.coalitions
    
    def get_coalitions_with_multiple_players(self, number_players:int):
        if number_players == len(self.graph.get_players()):
            return
        
        player_orders = list(itertools.combinations(self.player_labels, number_players))
        for order in player_orders:
            player_to_a = False
            nodes_to_a = []
            player_to_b = False
            nodes_to_b = []
            coalition_key = ''
            for player_label in order:
                coalition_key += str(player_label)
                if player_label in self.source_a_set:
                    player_to_a = True
                    nodes_to_a.append(player_label)
                elif player_label in self.source_b_set:
                    player_to_b = True
                    nodes_to_b.append(player_label)
            coalition_cost = 0
            if player_to_a:
                edges_to_a = self.getEdgesBetweenPlayersAndSource(nodes_to_a, 'a')
                mcst_a = MCST(Graph(edges_to_a, self.graph.get_sources(), self.graph.get_players()))
                _, mcst_cost_a = mcst_a.kruskal()
                coalition_cost += mcst_cost_a
            
            if player_to_b:
                edges_to_b = self.getEdgesBetweenPlayersAndSource(nodes_to_b, 'b')
                mcst_b = MCST(Graph(edges_to_b, self.graph.get_sources(), self.graph.get_players()))
                _, mcst_cost_b = mcst_b.kruskal()
                coalition_cost += mcst_cost_b
            self.coalitions[coalition_key] = coalition_cost
        self.get_coalitions_with_multiple_players(number_players=number_players+1)

    
    # TESTED
    def getEdgesBetweenPlayersAndSource(self, players:list, source:str):
        edges = []
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if (start_label in players or start_label == source) and (end_label in players or end_label == source):
                edges.append(edge)
        return edges

    # TESTED
    def getEdgeWithEndpoints(self, endpoint1, endpoint2) -> Edge:
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if (start_label == endpoint1 or end_label == endpoint1) and (start_label == endpoint2 or end_label == endpoint2):
                return edge
