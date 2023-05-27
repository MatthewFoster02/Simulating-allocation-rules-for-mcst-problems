from graph.graph import Graph
from graph.edge import Edge

class MCST:
    def __init__(self, graph:Graph):
        self.edges = graph.get_edges()
        self.sort_edges_by_cost()
        sources = graph.get_sources()
        players = graph.get_players()
        self.sets = []
        for source in sources:
            self.sets.append({source.get_label()})
        for player in players:
            self.sets.append({player.get_label()})

    def sort_edges_by_cost(self):
        self.edges.sort(key=lambda edge: edge.get_cost())
    
    def kruskal(self):
        total_cost = 0
        mcst_edges = []

        for edge in self.edges:
            if(self.is_cycle_created(edge)): # Guard clause - if cycle generated, then skip edge
                continue

            total_cost += edge.get_cost()
            mcst_edges.append(edge)
        
        return mcst_edges, total_cost
    
    def is_cycle_created(self, edge:Edge):
        node_u = edge.get_start_node()
        node_v = edge.get_end_node()

        for node_set in self.sets:
            if node_u.get_label() in node_set and node_v.get_label() in node_set:
                print('CYCLE')
                return True
        
        node_u_set, node_v_set = self.find_sets(node_u.get_label(), node_v.get_label())
        print(f'Joining sets - {node_u_set}, {node_v_set}')
        self.join_sets(node_u_set, node_v_set)
    
    def find_sets(self, node_u_label, node_v_label):
        node_u_set = set()
        node_v_set = set()
        for node_set in self.sets:
            if node_u_label in node_set:
                node_u_set = node_set
            if node_v_label in node_set:
                node_v_set = node_set
        
        return node_u_set, node_v_set

    def join_sets(self, node_u_set:set, node_v_set:set):
        combined_set = node_u_set.union(node_v_set)

        for node_set in self.sets:
            if node_u_set.intersection(node_set) or node_v_set.intersection(node_set):
                self.sets.remove(node_set)
        
        self.sets.append(combined_set)
        print(f'Joined sets! Sets = {self.sets}')
            

