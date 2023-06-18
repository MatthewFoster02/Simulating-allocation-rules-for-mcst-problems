import random

from graph.graph import Graph
from graph.node import Node
from first_rule_and_prims.mcst import MCST
from cooperative_functions.cooperative_gt import CoopMethods
from cooperative_functions.shapley_value import ShapleyValue
from irreducibililty.regular_reduce import RegularReduce
from irreducibililty.fix_over_reduce import FixOverReduce



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
    limit = 1000000

    contradiction_counter = 0
    two_component_optimal_counter = 0
    overreduced = 0
    fixed_overreduced = 0
    contra_4s = 0

    current_percentage = 0.0
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

        coop_original_graph = CoopMethods(graph=graph)

        coalitions_original_graph = coop_original_graph.get_player_coalition_values(source_a_set, source_b_set)

        rr = RegularReduce(graph=graph, mcst_edges=mcst_edges)
        reduced_graph = rr.reduce_graph()
        
        fix = FixOverReduce(reduced_graph=reduced_graph, mcst_edges=mcst_edges, original_graph=graph, original_coalitions=coalitions_original_graph, source_a_set=source_a_set, source_b_set=source_b_set)
        if fix.is_over_reduced(reduced_graph):
            overreduced += 1

            coop_reduced_graph = CoopMethods(graph=reduced_graph)
            coalitions_reduced_graph = coop_reduced_graph.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
        
            fixed_graph = fix.fix_over_reduce()
            coop_fixed_graph = CoopMethods(graph=fixed_graph)
            coalitions_fixed_graph = coop_fixed_graph.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
            
            if not fix.is_over_reduced(fixed_graph):
                fixed_overreduced += 1
                sv = ShapleyValue(coalitions_fixed_graph, len(graph.get_players()))
                shapley_value = sv.get_shapley_value()

                if not coop_original_graph.belongs_to_core(coalitions_original_graph, shapley_value):
                    if len(graph.get_players()) == 4 and coalitions_original_graph['4'] == shapley_value[3]:
                        contra_4s += 1
                    else:
                        contradiction_counter += 1
                        data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {coalitions_original_graph}
Coalitions (Reduced): {coalitions_reduced_graph}
Coalitions (Fixed): {coalitions_fixed_graph}
Allocation {shapley_value} not in core...
Reduced Graph:
{reduced_graph.to_string()}
Fixed Graph:
{fixed_graph.to_string()}\n\n"""
                        with open('not_fixed.txt', 'a') as file:
                            file.write(data)

        limiter += 1
        percent_complete = round((limiter/limit)*100, 2)
        if not percent_complete == current_percentage:
            current_percentage = percent_complete
            print(f'{current_percentage}% complete...')

    print('DONE')
    print(f'\nOverall: {contradiction_counter}/{limit} CONTRADICTIONS')
    print(f'\n4 issue: {contra_4s}/{limit} CONTRADICTIONS')
    # print(f'\nOverall: {overreduced-fixed_overreduced}/{limit} CONTRADICTIONS')
    # print(f'\nOverreduced amount: {overreduced}/{limit}')
    # print(f'\nOverreduced fixed amount: {fixed_overreduced}/{limit}')
    print(f'{two_component_optimal_counter} times a randomly generated graph had 2 components in the optimal solution. {limiter+two_component_optimal_counter}')

