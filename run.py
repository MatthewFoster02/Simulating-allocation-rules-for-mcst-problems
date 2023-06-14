import random

from graph.graph import Graph
from graph.node import Node
from mcst import MCST
from cooperative_functions.cooperative_gt import CoopMethods
from path_checking_rule import PathRule

# TESTED
def get_random_source_sets(players:list[Node]):
    source_a_set = set()
    source_b_set = set()
    number_of_players = len(players)
    for i, player in enumerate(players):
        if not i == number_of_players-1:
            if random.random() < 0.5:
                source_a_set.add(player.get_label())
                continue
            
            source_b_set.add(player.get_label())
            continue

        if len(source_a_set) == 0:
            source_a_set.add(player.get_label())
            continue
        
        if len(source_b_set) == 0:
            source_b_set.add(player.get_label())
            continue

        if random.random() < 0.5:
            source_a_set.add(player.get_label())
            continue
            
        source_b_set.add(player.get_label())
    
    return source_a_set, source_b_set
        
# TESTED
def get_mcst_cost_subgraph(graph:Graph, source_set:set, source:str):
    coop = CoopMethods(graph=graph)
    sub_graph_edges = coop.getEdgesBetweenPlayersAndSource(source_set, source)

    graph_players = []
    for player_label in source_set:
        graph_players.append(Node(label=player_label))
    
    graph_mcst = MCST(graph=Graph(sub_graph_edges, sources=[Node(type='source', label=source)], players=graph_players))
    _, graph_mcst_cost = graph_mcst.kruskal()
    return graph_mcst_cost

def will_optimal_solution_have_2_components(mcst:MCST, graph:Graph, source_a_set:set, source_b_set:set):
    # Check if graph will have 1 component optimal solution
    _, mcst_full_cost = mcst.kruskal()
    mcst_a_cost = get_mcst_cost_subgraph(graph, source_a_set, 'a')
    mcst_b_cost = get_mcst_cost_subgraph(graph, source_b_set, 'b')
    #print(f'S = {mcst_full_cost}. Sa = {mcst_a_cost}. Sb = {mcst_b_cost}.')
    return mcst_full_cost > mcst_a_cost + mcst_b_cost
    

def run():
    type_rule = int(input('Enter rule number:\n1. Original\n2. Prims\n3. Path\n'))
    limiter = 0
    limit = 1000000

    contradiction_counter = 0
    two_component_optimal_counter = 0

    current_percentage = 0
    while limiter < limit:
        graph = Graph()
        if random.random() < 0.5:
            graph.generate_random_graph()
        else:
            graph.generate_random_graph(num_players=4)
        source_a_set, source_b_set = get_random_source_sets(graph.get_players())

        mcst_instance = MCST(graph=graph, source_a_set=source_a_set, source_b_set=source_b_set)
        mcst_edges, _ = mcst_instance.kruskal()

        if will_optimal_solution_have_2_components(mcst_instance, graph, source_a_set, source_b_set):
            two_component_optimal_counter += 1
            #print(f'\nGraph has optimal solution with 2 components, skipping...\n')
            continue

        coop = CoopMethods(graph=graph)

        coalitions = coop.get_player_coalition_values(source_a_set, source_b_set)

        # Get allocation using path rule
        if(type_rule == 3):
            pathRule = PathRule(graph=graph, mcst_edges=mcst_edges, source_a_set=source_a_set, source_b_set=source_b_set)
            solution = pathRule.run_rule()
            if not solution:
                allocation = pathRule.get_cost_allocation()
            else:
                type_rule = 1
                
        
        # Get allocation using kruskal and prim.
        if(type_rule == 2):
            mcst_instance.kruskal()
            mcst_instance.prim()
            allocation = mcst_instance.getCostAllocation()

        # Original
        if(type_rule == 1):
            mcst_instance.kruskal()
            mcst_instance.kruskal(share_edge_costs=True)
            allocation = mcst_instance.getCostAllocation()

        if not coop.belongs_to_core(coalitions, allocation):
            contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {coalitions}
Allocation: {allocation}
Allocation not in core of game...
Sum of cost allocation and grand coalition cost: {sum(allocation)} != {list(coalitions.values())[-1]}\n\n"""
            with open('contradictions.txt', 'a') as file:
                file.write(data)

        limiter += 1
        percent_complete = round((limiter/limit)*100)
        if not percent_complete == current_percentage:
            current_percentage = percent_complete
            print(f'{current_percentage}% complete...')

    print('DONE')
    print(f'\nOverall: {contradiction_counter}/{limit} CONTRADICTIONS')
    print(f'{two_component_optimal_counter} times a randomly generated graph had 2 components in the optimal solution. {limiter+two_component_optimal_counter}')
