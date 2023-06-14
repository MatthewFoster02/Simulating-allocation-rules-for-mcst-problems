import random

from graph.graph import Graph
from mcst import MCST
from cooperative_functions.cooperative_gt import CoopMethods

def run():
    limit = 100
    limiter = 0

    contradiction_counter = 0

    while limiter < limit:
        graph = Graph()
        if random.random() < 0.5:
            graph.generate_random_graph(num_sources=1)
        else:
            graph.generate_random_graph(num_sources=1, num_players=4)
        
        kruskal = MCST(graph=graph)
        kruskal.kruskal(use_classical_folk_rule=True)
        cost_allocation = kruskal.getCostAllocation()

        coop = CoopMethods(graph=graph)
        coalitions = coop.get_coalitions_one_source()

        if not coop.belongs_to_core(coalitions, cost_allocation):
            contradiction_counter += 1
            data = f"""
CONTRADICTION on graph number {limiter}:\n
Graph Edges:
{graph.to_string()}
Coalitions: {coalitions}
Allocation: {cost_allocation}
Allocation not in core of game...\n\n"""
            print(data)
        
        limiter += 1
        print(f'{limiter}/{limit} complete...')
        if not sum(cost_allocation) == list(coalitions.values())[-1]:
            print(f'\nBTW Sum of cost allocation not equal to grand coalition cost. {sum(cost_allocation)} != {list(coalitions.values())[-1]}')
    
    print('DONE!')
    
    print(f'\n{contradiction_counter}/{limit} CONTRADICTIONS')
