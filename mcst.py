from graph.graph import Graph
from graph.edge import Edge

class MCST:
    def __init__(self, graph:Graph, source_a_set:set = set(), source_b_set:set = set()):
        self.edges = graph.get_edges()
        self.sort_edges_by_cost()
        self.sources = graph.get_sources()
        self.players = graph.get_players()
        self.sets = self.generate_sets()
        self.source_a_set = source_a_set
        self.source_b_set = source_b_set
        self.cost_allocation = [0] * len(self.players)
    



    def generate_sets(self):
        components = []
        for source in self.sources:
            components.append({source.get_label()})
        for player in self.players:
            components.append({player.get_label()})
        return components

    # TESTED
    def sort_edges_by_cost(self):
        self.edges.sort(key=lambda edge: edge.get_cost())
    
    # TESTED
    def kruskal(self, share_edge_costs:bool = False):
        # ensure sets are reset
        self.sets = self.generate_sets()
        total_cost = 0
        mcst_edges = []

        for edge in self.edges:
            if(self.is_cycle_created(edge)): # Guard clause - if cycle generated, then skip edge
                continue


            total_cost += edge.get_cost()
            mcst_edges.append(edge)
            if share_edge_costs:
                self.share_cost_of_edge(edge)
            
            # Update state
            node_u_set, node_v_set = self.find_sets(edge.get_start_node().get_label(), edge.get_end_node().get_label())
            self.join_sets(node_u_set, node_v_set)
        
        self.mcst = mcst_edges
        self.mcst_cost = total_cost
        return mcst_edges, total_cost
    
    # TESTED
    def is_cycle_created(self, edge:Edge):
        node_u = edge.get_start_node()
        node_v = edge.get_end_node()

        for node_set in self.sets:
            if node_u.get_label() in node_set and node_v.get_label() in node_set:
                return True
        return False
    
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
    
    # TESTED
    def share_cost_of_edge(self, edge:Edge):
        start_node = edge.get_start_node()
        end_node = edge.get_end_node()
        start_node_set, end_node_set = self.find_sets(start_node.get_label(), end_node.get_label())

        join_type = self.determineJoiningComponents(start_node.get_label(), end_node.get_label())
        # Switch
        if join_type == 'nosource': # Case 1: no sources
            self.share_proportionately(start_node_set, end_node_set, edge.get_cost())
        
        elif join_type == 'onesource': # Case 2: 1 source
            sourceless_set, set_with_source = self.find_set_without_source(start_node_set, end_node_set)
            beneficiaries = self.checkBenefiting(sourceless_set, set_with_source)
            if not len(beneficiaries) == 0: # 2.a: Sourceless component benefits
                self.share_evenly(beneficiaries, edge.get_cost())
            else: # 2.b: No beneficiaries
                self.remove_check_disconnected(edge, edge.get_cost())

        elif join_type == 'bothsources': # Case 3: Both components 1 source
            beneficiaries_start_set = self.checkBenefiting(start_node_set, end_node_set)
            beneficiaries_end_set = self.checkBenefiting(end_node_set, start_node_set)

            start_set_not_empty = not len(beneficiaries_start_set) == 0
            end_set_not_empty = not len(beneficiaries_end_set) == 0

            if start_set_not_empty and end_set_not_empty: # 3.a: Both components benefitting
                self.share_proportionately(beneficiaries_start_set, beneficiaries_end_set, edge.get_cost())
            elif start_set_not_empty: # 3.b: 1 component benefitting
                self.share_evenly(beneficiaries_start_set, edge.get_cost())
            elif end_set_not_empty: # 3.b: 1 component benefitting
                self.share_evenly(beneficiaries_end_set, edge.get_cost())
            else: # 3.c: No beneficiaries
                self.remove_check_disconnected(edge, edge.get_cost())
        
        elif join_type == '2sources':
            sourceless_set, _ = self.find_set_without_source(start_node_set, end_node_set)
            self.share_evenly(sourceless_set, edge.get_cost())
    
    # TESTED
    def determineJoiningComponents(self, start_node_label, end_node_label):
        start_component, end_component = self.find_sets(start_node_label, end_node_label)

        if self.hasSource(start_component) and self.hasSource(end_component):
            return 'bothsources'
        elif self.oneHasOneSource(start_component, end_component):
            return 'onesource'
        elif self.hasBothSources(start_component) or self.hasBothSources(end_component):
            return '2sources'
        
        return 'nosource'
    
    # TESTED
    def hasSource(self, component:set):
        return component.intersection({'a'}) or component.intersection({'b'})
    
    # TESTED
    def oneHasOneSource(self, first_component:set, second_component:set):
        return ( (self.hasSource(first_component) and not self.hasSource(second_component) and not self.hasBothSources(first_component)) or # first source, second none AND first only 1 source
                (not self.hasSource(first_component) and self.hasSource(second_component) and not self.hasBothSources(second_component)) ) # first none, second source AND second only 1 source
    
    # TESTED
    def hasBothSources(self, component:set):
        return component.intersection({'a'}) and component.intersection({'b'})

    # TESTED
    def find_set_without_source(self, first_set:set, second_set:set):
        if first_set.intersection({'a'}) or first_set.intersection({'b'}):
            return second_set, first_set
        return first_set, second_set
    
    # TESTED
    def checkBenefiting(self, set_to_check:set, other_set_with_source:set):
        # Establish what counts as benefiting
        check_source_a = self.has_this_source(other_set_with_source, {'a'})
        check_source_b = self.has_this_source(other_set_with_source, {'b'})

        beneficiaries = set()
        for node in set_to_check:
            if not type(node) == int:
                continue

            if check_source_a:
                if node in self.source_a_set:
                    beneficiaries.add(node)
            
            if check_source_b:
                if node in self.source_b_set:
                    beneficiaries.add(node)
        
        return beneficiaries
    
    # TESTED
    def has_this_source(self, component:set, source:set):
        return component.intersection(source)

    # TESTED
    def remove_check_disconnected(self, edge:Edge, cost:float):
        new_graph = Graph(self.mcst)
        edges_new_graph = new_graph.get_edges()
        for new_edge in edges_new_graph:
            if ( new_edge.get_start_node().get_label() == edge.get_start_node().get_label() and
                 new_edge.get_end_node().get_label() == edge.get_end_node().get_label() ):
                edges_new_graph.remove(new_edge)
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
        first_component_without_sources = first_component - {'a', 'b'} # remove source from components
        second_component_without_sources = second_component - {'a', 'b'}
        joined_component = first_component_without_sources.union(second_component_without_sources) # Get joined component
        joined_component_size = len(joined_component)
        for player in self.players: # Loop through players to determine cost sharing
            if not player.get_label() in joined_component:
                continue # If player not invlovled skip (pays nothing)

            player_component = set() # Find player set and its length
            if player.get_label() in first_component_without_sources:
                player_component = first_component_without_sources
            elif player.get_label() in second_component_without_sources:
                player_component = second_component_without_sources
            player_component_size = len(player_component)

            joined_less_player = joined_component - player_component # Get size of joined set less player set
            top_row_fraction = len(joined_less_player) # Top row of fraction is this size
            bottom_row_franction = joined_component_size * player_component_size # Bottom row is joined set size * player set size
            self.cost_allocation[player.get_label()-1] = (top_row_fraction / bottom_row_franction) * cost_to_share # Player pays above fraction of the cost

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
    
    def setMCST(self, mcst:list[Edge]):
        self.mcst = mcst
    
    def getMCST(self):
        return self.mcst
    
    def setMCSTCost(self, mcst_cost:float):
        self.mcst_cost = mcst_cost
    
    def getMCSTCost(self):
        return self.mcst_cost
