from graph.graph import Graph
from mcst import MCST

graph = Graph()
graph.generate_random_graph()
print(graph.to_string())
graph.check_path_between_2_nodes(1, 'a')
mcst = MCST(graph=graph)
edges, total_cost = mcst.kruskal()

print(f'The total cost of the MCST is: {total_cost}')
print('Edges')
for edge in edges:
    print(edge.to_string())