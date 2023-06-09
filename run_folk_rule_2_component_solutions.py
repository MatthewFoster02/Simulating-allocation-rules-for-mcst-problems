import random

from graph.node import Node
from graph.graph import Graph
from mcst import MCST
from cooperative_gt import CoopMethods
from run import will_optimal_solution_have_2_components, get_random_source_sets

# TESTED
def get_subgraph(graph:Graph, source_set:set, source_label:str) -> Graph:
    subgraph_edges = []
    for edge in graph.get_edges():
        start_node_label = edge.get_start_node().get_label()
        end_node_label = edge.get_end_node().get_label()
        if start_node_label in source_set and end_node_label in source_set: # If both labels are players wishing to connect to same source, add
            subgraph_edges.append(edge)
            continue
        
        if start_node_label in source_set and end_node_label == source_label: # If start label is player and end label is source, add
            subgraph_edges.append(edge)
            continue

        if start_node_label == source_label and end_node_label in source_set: # If start label is source and end label is player, add
            subgraph_edges.append(edge)

    source = Node(type='source', label=source_label)
    players = []
    for player_label in source_set:
        player = Node(label=player_label)
        players.append(player)
    
    return Graph(edges=subgraph_edges, sources=[source], players=players)

# TESTED
def join_sub_allocations(allocation_a:list[float], allocation_b:list[float], source_a_set:set, source_b_set:set):
    combined_len = len(allocation_a) + len(allocation_b)
    combined_allocation = [0] * combined_len

    for i, player_label in enumerate(source_a_set):
        combined_allocation[player_label-1] = allocation_a[i]
    
    for i, player_label in enumerate(source_b_set):
        combined_allocation[player_label-1] = allocation_b[i]
    return combined_allocation



def run():
    limit = 1000000
    limiter = 0

    graph_a_contradiction_counter = 0
    graph_b_contradiction_counter = 0
    contradiction_counter = 0

    current_percentage = 0
    while limiter < limit:
        graph = Graph()
        if random.random() < 0.5:
            graph.generate_random_graph()
        else:
            graph.generate_random_graph(num_players=4)
        source_a_set, source_b_set = get_random_source_sets(graph.get_players())
        
        mcst_instance = MCST(graph=graph, source_a_set=source_a_set, source_b_set=source_b_set)
        if not will_optimal_solution_have_2_components(mcst=mcst_instance, graph=graph, source_a_set=source_a_set, source_b_set=source_b_set):
            #print('Solution has one component, skipping...')
            continue

        graph_a = get_subgraph(graph, source_a_set, 'a')
        graph_b = get_subgraph(graph, source_b_set, 'b')

        coop_full_graph = CoopMethods(graph=graph)
        coop_graph_a = CoopMethods(graph=graph_a)
        coop_graph_b = CoopMethods(graph=graph_b)

        graph_a_coalitions = coop_graph_a.get_coalitions_one_source('a')
        graph_b_coalitions = coop_graph_b.get_coalitions_one_source('b')
        full_graph_coalitions = coop_full_graph.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)

        # Get allocations
        kruskal_a = MCST(graph=graph_a)
        kruskal_a.kruskal(use_classical_folk_rule=True)
        allocation_a = kruskal_a.getCostAllocation()

        # if not coop_graph_a.belongs_to_core(graph_a_coalitions, allocation_a):
        #     graph_a_contradiction_counter += 1
        #     print(f'Subgraph a folk allocation not in core... {sum(allocation_a)} and {list(graph_a_coalitions.values())[-1]}')

        kruskal_b = MCST(graph=graph_b)
        kruskal_b.kruskal(use_classical_folk_rule=True)
        allocation_b = kruskal_b.getCostAllocation()

        # if not coop_graph_b.belongs_to_core(graph_b_coalitions, allocation_b):
        #     graph_b_contradiction_counter += 1
        #     print(f'Subgraph b folk allocation not in core... {sum(allocation_b)} and {list(graph_b_coalitions.values())[-1]}')
        
        full_graph_allocation = join_sub_allocations(allocation_a, allocation_b, source_a_set, source_b_set)

        if not coop_full_graph.belongs_to_core(full_graph_coalitions, full_graph_allocation):
            contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Source A: {source_a_set} Source B: {source_b_set}
Coalitions: {full_graph_coalitions}
Allocation: {full_graph_allocation}
Allocation not in core of game...
Sum of cost allocation and grand coalition cost: {sum(full_graph_allocation)} and {list(full_graph_coalitions.values())[-1]}
Graph A:
{graph_a.to_string()} {graph_a_coalitions} {allocation_a}
Graph B:
{graph_b.to_string()} {graph_b_coalitions} {allocation_b}\n\n"""
            with open('contradictions.txt', 'a') as file:
                file.write(data)
        
        limiter += 1
        percent_complete = round((limiter/limit)*100)
        if not percent_complete == current_percentage:
            current_percentage = percent_complete
            print(f'{current_percentage}% complete...')

    print('DONE')
    print(f'\n{contradiction_counter}/{limit} CONTRADICTIONS')
    print(f'\n{graph_a_contradiction_counter}/{limit} SUBGRAPH A CONTRADICTIONS')
    print(f'\n{graph_b_contradiction_counter}/{limit} SUBGRAPH B CONTRADICTIONS')

run()
