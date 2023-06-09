import itertools
import numpy as np

from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from mcst import MCST

class CoopMethods:
    def __init__(self, graph:Graph = None):
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
            self.coalitions[''.join(map(str, self.player_labels))] = mcst_full_graph_cost
        else:
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

            coalition_cost_a = 0
            coalition_cost_b = 0
            coalition_cost_full = 100000000
            if player_to_a:
                edges_to_a = self.getEdgesBetweenPlayersAndSource(nodes_to_a, 'a')
                mcst_a = MCST(Graph(edges_to_a, self.graph.get_sources(), self.graph.get_players()))
                _, mcst_cost_a = mcst_a.kruskal()
                coalition_cost_a = mcst_cost_a
            
            if player_to_b:
                edges_to_b = self.getEdgesBetweenPlayersAndSource(nodes_to_b, 'b')
                mcst_b = MCST(Graph(edges_to_b, self.graph.get_sources(), self.graph.get_players()))
                _, mcst_cost_b = mcst_b.kruskal()
                coalition_cost_b = mcst_cost_b
            
            if player_to_a and player_to_b:
                edges_to_a = self.getEdgesBetweenPlayersAndSource(nodes_to_a, 'a')
                edges_to_b = self.getEdgesBetweenPlayersAndSource(nodes_to_b, 'b')
                edge_a_to_b = self.getEdgeBetweenSources()
                all_edges = edges_to_a + edges_to_b
                all_edges.append(edge_a_to_b)
                mcst_all_edges = MCST(Graph(all_edges, self.graph.get_sources(), self.graph.get_players()))
                _, mcst_all_edges_cost = mcst_all_edges.kruskal()
                coalition_cost_full = mcst_all_edges_cost

            if coalition_cost_full <= coalition_cost_a + coalition_cost_b:
                coalition_cost = coalition_cost_full
            else:
                coalition_cost = coalition_cost_a + coalition_cost_b

            self.coalitions[coalition_key] = coalition_cost
        self.get_coalitions_with_multiple_players(number_players=number_players+1)
    
    def get_coalitions_one_source(self, source_label:str):
        # SINGLE PLAYER COALITIONS
        self.player_labels = []
        self.coalitions = {}
        self.source_label = source_label
        for player in self.graph.get_players():
            self.coalitions[str(player.get_label())] = self.getEdgeWithEndpoints(player.get_label(), source_label).get_cost()
            self.player_labels.append(player.get_label())
        
        # MULTI-PLAYER COALITIONS
        if len(self.graph.get_edges()) > 2:
            self.get_coalitions_with_multiple_players_one_source(2)

        # GRAND COALITION
        kruskal = MCST(graph=self.graph)
        _, grand_coalition_cost = kruskal.kruskal()

        self.coalitions[''.join(map(str, self.player_labels))] = grand_coalition_cost
        return self.coalitions
    
    def get_coalitions_with_multiple_players_one_source(self, number_players:int):
        if number_players == len(self.graph.get_players()):
            return
        
        player_orders = list(itertools.combinations(self.player_labels, number_players))
        for order in player_orders:
            edges = self.getEdgesBetweenPlayersAndSource(list(order), self.source_label)
            kruskal = MCST(Graph(edges, self.graph.get_sources(), self.graph.get_players()))
            _, coalition_cost = kruskal.kruskal()
            self.coalitions[''.join(str(x) for x in order)] = coalition_cost
        self.get_coalitions_with_multiple_players_one_source(number_players=number_players+1)
    
    # TESTED
    def getEdgesBetweenPlayersAndSource(self, players:list, source:str):
        edges = []
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if (start_label in players or start_label == source) and (end_label in players or end_label == source):
                edges.append(edge)
        return edges
    
    def getEdgeBetweenSources(self):
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if start_label == 'a' and end_label == 'b':
                return edge

    # TESTED
    def getEdgeWithEndpoints(self, endpoint1, endpoint2) -> Edge:
        for edge in self.graph.get_edges():
            start_label = edge.get_start_node().get_label()
            end_label = edge.get_end_node().get_label()
            if start_label == endpoint1 and end_label == endpoint2: # If start label is endpoint1 and end label is endpoint2, found ege!
                return edge
            if start_label == endpoint2 and end_label == endpoint1: # If start label is endpoint2 and end label is endpoint1, found edge!
                return edge
    
    def belongs_to_core(self, coalitions:dict, allocation:list):
        if len(coalitions) == 7:
            return self.belongs_to_core_3_players(coalitions, allocation)
        elif len(coalitions) == 15:
            return self.belongs_to_core_4_players(coalitions, allocation)
        else:
            raise 'Game must have either 3 or 4 players, ie dictionary with 7 or 15 entries corresponding to the coalitions'
    
    def belongs_to_core_3_players(self, coalitions:dict, allocation:list):
        if not len(allocation) == 3:
            raise 'Allocation must be of length 3, as there are 3 players'
        
        # Convert to cost game allocation
        allocation = [-x for x in allocation]
        # Remove redundant final allocation
        modified_allocation = np.array(allocation[:2])
        c1 = coalitions['1']
        c2 = coalitions['2']
        c3 = coalitions['3']
        c12 = coalitions['12']
        c13 = coalitions['13']
        c23 = coalitions['23']
        c123 = coalitions['123']
        # Convert to costs
        c1*=-1
        c2*=-1
        c3*=-1
        c12*=-1
        c13*=-1
        c23*=-1
        c123*=-1

        core_region = np.array([ [1, 0],
                            [-1, 0],
                            [0, 1],
                            [0, -1],
                            [1, 1],
                            [-1, -1]])

        b = np.array([c1,
                      -c123 + c23,
                      c2,
                      -c123 + c13,
                      c12,
                      -c123 + c3])
        
        point = np.dot(core_region, modified_allocation.T) - b.T

        return all(x >= 0 for x in point) # If all elements are >= 0, point is in core
    
    def belongs_to_core_4_players(self, coalitions:dict, allocation:list):
        if not len(allocation) == 4:
            raise 'Allocation must be of length 4, as there are 4 players'
        
        # Convert to cost game allocation
        allocation = [-x for x in allocation]
        # Remove redundant final allocation
        modified_allocation = np.array(allocation[:3])
        c1 = coalitions['1']
        c2 = coalitions['2']
        c3 = coalitions['3']
        c4 = coalitions['4']
        c12 = coalitions['12']
        c13 = coalitions['13']
        c14 = coalitions['14']
        c23 = coalitions['23']
        c24 = coalitions['24']
        c34 = coalitions['34']
        c123 = coalitions['123']
        c124 = coalitions['124']
        c134 = coalitions['134']
        c234 = coalitions['234']
        c1234 = coalitions['1234']
        # Convert to costs
        c1*=-1
        c2*=-1
        c3*=-1
        c4*=-1
        c12*=-1
        c13*=-1
        c14*=-1
        c23*=-1
        c24*=-1
        c34*=-1
        c123*=-1
        c124*=-1
        c134*=-1
        c234*=-1
        c1234*=-1

        core_region = np.array([[1, 0, 0],
                                [-1, 0, 0],
                                [0, 1, 0],
                                [0, -1, 0],
                                [0, 0, 1],
                                [0, 0, -1],
                                [1, 1, 1],
                                [-1, -1, -1],
                                [1, 1, 0],
                                [-1, -1, 0],
                                [1, 0, 1],
                                [-1, 0, -1],
                                [0, 1, 1],
                                [0, -1, -1]])

        b = np.array([c1,
                    -c1234 + c234,
                    c2,
                    -c1234 + c134,
                    c3,
                    -c1234 + c124,
                    c123,
                    -c1234 + c4-0.05,
                    c12,
                    -c1234 + c34,
                    c13,
                    -c1234 + c24,
                    c23,
                    -c1234 + c14])
        
        point = np.dot(core_region, modified_allocation.T) - b.T
        print(point)
        return all(x >= 0 for x in point) # If all elements are >= 0, point is in core

