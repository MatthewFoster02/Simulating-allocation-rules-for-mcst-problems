from graph.node import Node
from graph.edge import Edge

class FolkRule:
    def __init__(self, source:Node, players:list[Node]):
        self.source = source
        self.players = players
        self.cost_allocation = {key.get_label(): 0 for key in players}
    
    # TESTED
    def share_edge_cost(self, edge:Edge, current_components:list[set]):
        self.current_components = current_components
        start_node_label = edge.get_start_node().get_label()
        end_node_label = edge.get_end_node().get_label()
        start_node_component = self.get_component_of_node(start_node_label)
        end_node_component = self.get_component_of_node(end_node_label)

        component_with_source = self.get_component_with_source(start_node_component, end_node_component) # Might return None
        if component_with_source is None:
            self.share_proportionately(start_node_component, end_node_component, edge.get_cost())
            return
        
        if component_with_source == start_node_component:
            self.share_evenly(end_node_component, edge.get_cost())
            return
        
        if component_with_source == end_node_component:
            self.share_evenly(start_node_component, edge.get_cost())
            return
    
    # TESTED
    def get_component_of_node(self, node_label):
        for component in self.current_components:
            if node_label in component:
                return component

    # TESTED
    def get_component_with_source(self, first_component:set, second_component:set):
        for label in first_component:
            if label == self.source.get_label():
                return first_component
        
        for label in second_component:
            if label == self.source.get_label():
                return second_component
        
        return None

    # TESTED
    def share_proportionately(self, first_component:set, second_component:set, cost_to_share:float):
        joined_component = first_component.union(second_component) # Get joined component
        joined_component_size = len(joined_component)

        for player in self.players: # Loop through players to determine cost sharing
            if not player.get_label() in joined_component:
                continue # If player not invlovled skip (pays nothing)

            player_component = set() # Find player set and its length
            if player.get_label() in first_component:
                player_component = first_component
            elif player.get_label() in second_component:
                player_component = second_component
            player_component_size = len(player_component)

            joined_less_player = joined_component - player_component # Get size of joined set less player set
            top_row_fraction = len(joined_less_player) # Top row of fraction is this size
            bottom_row_franction = joined_component_size * player_component_size # Bottom row is joined set size * player set size
            self.cost_allocation[player.get_label()] += (top_row_fraction / bottom_row_franction) * cost_to_share # Player pays above fraction of the cost

    # TESTED
    def share_evenly(self, component:set, cost_to_share:float):
        number_player_sharing = len(component)
        cost_split = cost_to_share/number_player_sharing

        for player_label in component:
            self.cost_allocation[player_label] += cost_split # Update allocation of players sharing cost

    # BOILERPLATE
    def get_cost_allocation(self):
        return list(self.cost_allocation.values())

    def set_components(self, components:list[set]):
        self.current_components = components   
