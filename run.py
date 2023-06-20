import random
import time

from graph.graph import Graph
from graph.node import Node
from first_rule_and_prims.mcst import MCST
from cooperative_functions.cooperative_gt import CoopMethods
from path_rule.path_checking_rule import PathRule

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
    limiter = 0
    limit = 100

    path_contradiction_counter = 0
    prim_contradiction_counter = 0
    kruskal_contradiction_counter = 0
    two_component_optimal_counter = 0
    path_rule_couldnt_compute = 0

    kruskal_time = 0
    prim_time = 0
    path_time = 0

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
        
        pathRule = PathRule(graph=graph, mcst_edges=mcst_edges, source_a_set=source_a_set, source_b_set=source_b_set)
        path_start = time.time()
        solution = pathRule.run_rule()
        path_end = time.time()
        path_time += (path_end - path_start) * 1000
        path_allocation_worked = False
        if not solution:
            path_rule_couldnt_compute += 1
        else:
            path_allocation = pathRule.get_cost_allocation()
            path_allocation_worked = True
                
        
        # Get allocation using kruskal and prim.
        prim_start = time.time()
        mcst_instance.kruskal()
        mcst_instance.prim()
        prim_end = time.time()
        prim_time += (prim_end - prim_start) * 1000
        prim_allocation = mcst_instance.getCostAllocation()

        # Original
        mcst_instance.resetCostAllocation()
        mcst_instance.kruskal()
        kruskal_start = time.time()
        mcst_instance.kruskal(share_edge_costs=True)
        kruskal_end = time.time()
        kruskal_time += (kruskal_end - kruskal_start) * 1000
        kruskal_allocation = mcst_instance.getCostAllocation()

        # Check path allocation
        if path_allocation_worked and not coop.belongs_to_core(coalitions, path_allocation):
            path_contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {coalitions}
Allocation: {path_allocation}
Allocation not in core of game...
Sum of cost allocation and grand coalition cost: {sum(path_allocation)} != {list(coalitions.values())[-1]}\n\n"""
            with open('path_contradictions.txt', 'a') as file:
                file.write(data)

        # Check prim allocation
        if not coop.belongs_to_core(coalitions, prim_allocation):
            prim_contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {coalitions}
Allocation: {prim_allocation}
Allocation not in core of game...
Sum of cost allocation and grand coalition cost: {sum(prim_allocation)} != {list(coalitions.values())[-1]}\n\n"""
            with open('prim_contradictions.txt', 'a') as file:
                file.write(data)

        # Check kruskal allocation
        if not coop.belongs_to_core(coalitions, kruskal_allocation):
            kruskal_contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {coalitions}
Allocation: {kruskal_allocation}
Allocation not in core of game...
Sum of cost allocation and grand coalition cost: {sum(kruskal_allocation)} != {list(coalitions.values())[-1]}\n\n"""
            with open('kruskal_contradictions.txt', 'a') as file:
                file.write(data)

        limiter += 1
        percent_complete = round((limiter/limit)*100)
        if not percent_complete == current_percentage:
            current_percentage = percent_complete
            print(f'{current_percentage}% complete...')

    print('DONE')
    print(f'\nOverall: {kruskal_contradiction_counter}/{limit} CONTRADICTIONS when using Kruskal')
    print(f'\nOverall: {prim_contradiction_counter}/{limit} CONTRADICTIONS when using Prim')
    print(f'\nOverall: {path_contradiction_counter}/{limit} CONTRADICTIONS when using Path')
    print(f'{two_component_optimal_counter} times a randomly generated graph had 1 components in the optimal solution. {limiter+two_component_optimal_counter}')
    print()
    print(f'Kruskal time: {kruskal_time}')
    print(f'Prim time: {prim_time}')
    print(f'Path time: {path_time}')