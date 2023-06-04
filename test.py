from graph.graph import Graph
from mcst import MCST
from cooperative_gt import CoopMethods

graph = Graph()
graph.generate_random_graph()
print(graph.to_string())

# coop = CoopMethods(graph)
# coalitions = coop.get_player_coalition_values({1, 4}, {2, 3})
# print(coalitions)


#graph.check_path_between_2_nodes(1, 'a')
mcst = MCST(graph=graph)
_, total_cost = mcst.kruskal()
# mcst.setMCST(edges)

_ = mcst.kruskal(share_edge_costs=True)



print(f'The total cost of the MCST is: {total_cost}')
print(f'Cost allocation: {mcst.getCostAllocation()}')
# print('Edges')
# for edge in edges:
#     print(edge.to_string())