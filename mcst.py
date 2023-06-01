from graph.graph import Graph
from graph.edge import Edge

class MCST:
    def __init__(self, graph:Graph, source_a_set:set = None, source_b_set:set = None):
        self.edges = graph.get_edges()
        self.sort_edges_by_cost()
        self.sources = graph.get_sources()
        self.players = graph.get_players()
        self.sets = []
        for source in self.sources:
            self.sets.append({source.get_label()})
        for player in self.players:
            self.sets.append({player.get_label()})
        
        self.source_a_set = source_a_set
        self.source_b_set = source_b_set
        self.cost_allocation = [0] * len(self.players)

    # TESTED
    def sort_edges_by_cost(self):
        self.edges.sort(key=lambda edge: edge.get_cost())
    
    # TESTED
    def kruskal(self, share_edge_costs:bool = False):
        total_cost = 0
        mcst_edges = []

        for edge in self.edges:
            if(self.is_cycle_created(edge)): # Guard clause - if cycle generated, then skip edge
                continue

            total_cost += edge.get_cost()
            mcst_edges.append(edge)
            if(share_edge_costs):
                self.share_cost_of_edge(edge)
        
        return mcst_edges, total_cost
    
    # TESTED
    def is_cycle_created(self, edge:Edge):
        node_u = edge.get_start_node()
        node_v = edge.get_end_node()

        for node_set in self.sets:
            if node_u.get_label() in node_set and node_v.get_label() in node_set:
                return True
        
        node_u_set, node_v_set = self.find_sets(node_u.get_label(), node_v.get_label())
        self.join_sets(node_u_set, node_v_set)
    
    # TESTED
    def find_sets(self, node_u_label, node_v_label):
        node_u_set = set()
        node_v_set = set()
        for node_set in self.sets:
            if node_u_label in node_set:
                node_u_set = node_set
            if node_v_label in node_set:
                node_v_set = node_set
        
        return node_u_set, node_v_set

    # TESTED
    def join_sets(self, node_u_set:set, node_v_set:set):
        combined_set = node_u_set.union(node_v_set)

        for node_set in self.sets:
            if node_u_set.intersection(node_set) or node_v_set.intersection(node_set):
                self.sets.remove(node_set)
        
        self.sets.append(combined_set)
            
    def share_cost_of_edge(self, edge):
        pass

    def remove_check_disconnected(self, edge:Edge, cost:float):
        new_graph = Graph(self.edges)
        edges_new_graph = new_graph.get_edges()
        edges_new_graph.remove(edge)
        new_graph.set_edges(edges_new_graph)

        disconnected_players = []
        for player in self.players:
            source_label = ''
            if player.get_label() in self.source_a_set:
                source_label = 'a'
            else:
                source_label = 'b'
            if not new_graph.check_path_between_2_nodes(player.get_label(), source_label):
                disconnected_players.append(player.get_label())
        
        if len(disconnected_players) == 0:
            return
        cost_split = cost/len(disconnected_players)
        for player in disconnected_players:
            self.cost_allocation[player-1] += cost_split

    # TESTED
    def share_proportionately(self, first_component:set, second_component:set, cost_to_share:float):
        cost_split = cost_to_share/2
        self.share_evenly(first_component, cost_split)
        self.share_evenly(second_component, cost_split)

    # TESTED
    def share_evenly(self, component:set, cost_to_share:float):
        number_player_sharing = len(component)
        cost_split = cost_to_share/number_player_sharing

        for player_label in component:
            self.cost_allocation[player_label-1] += cost_split # Update allocation of players sharing cost


    # BOILERPLATE
    def getEdges(self):
        return self.edges
    
    def setEdges(self, edges):
        self.edges = edges
    
    def getSourceASet(self):
        return self.source_a_set
    
    def setSourceASet(self, source_a_set):
        self.source_a_set = source_a_set
    
    def getSourceBSet(self):
        return self.source_b_set
    
    def setSourceBSet(self, source_b_set):
        self.source_b_set = source_b_set
    
    def setSets(self, new_set):
        self.sets = new_set
    
    def getSets(self):
        return self.sets
    
    def setCostAllocation(self, allocation):
        self.cost_allocation = allocation
    
    def getCostAllocation(self):
        return self.cost_allocation
