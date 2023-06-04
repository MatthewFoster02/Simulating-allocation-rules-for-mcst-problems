from graph.graph import Graph
from mcst import MCST
from cooperative_gt import CoopMethods

# graph = Graph()
# graph.generate_random_graph()
# print(graph.to_string())

coop = CoopMethods()
# coalitions = coop.get_player_coalition_values({1, 4}, {2, 3})
# print(coalitions)

print(coop.belongs_to_core({
    '1': 10,
    '2': 9,
    '3': 5,
    '4': 3,
    '12': 19,
    '13': 15,
    '14': 13,
    '23': 11,
    '24': 12,
    '34': 8,
    '123': 21,
    '124': 22,
    '134': 18,
    '234': 14,
    '1234': 19
}, [6, 6, 4, 3])
)


#graph.check_path_between_2_nodes(1, 'a')
# mcst = MCST(graph=graph)
# _, total_cost = mcst.kruskal()
# mcst.setMCST(edges)

# _ = mcst.kruskal(share_edge_costs=True)



# print(f'The total cost of the MCST is: {total_cost}')
# print(f'Cost allocation: {mcst.getCostAllocation()}')
# print('Edges')
# for edge in edges:
#     print(edge.to_string())