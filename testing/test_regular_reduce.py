from irreducibility.regular_reduce.py import RegularReduce
from graph.node import Node
from graph.edge import Edge

def test_get_max_cost_on_path_one_max():
    rr = RegularReduce()
    path = []
    path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=2))
    path.append(Edge(Node(label=1), Node(label=2), cost=7))
    path.append(Edge(Node(type='source', label='a'), Node(label=3), cost=4))
    assert rr.get_max_cost_on_path(path) == 7