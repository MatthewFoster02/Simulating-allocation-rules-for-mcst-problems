import pytest

from irreducibililty.regular_reduce import RegularReduce
from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph

@pytest.fixture
def graph():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 12))
    edges.append(Edge(node_source_a, node_player_1, 11))
    edges.append(Edge(node_source_a, node_player_2, 8))
    edges.append(Edge(node_source_a, node_player_3, 7))
    edges.append(Edge(node_source_b, node_player_1, 3))
    edges.append(Edge(node_source_b, node_player_2, 9))
    edges.append(Edge(node_source_b, node_player_3, 5))
    edges.append(Edge(node_player_1, node_player_2, 13))
    edges.append(Edge(node_player_1, node_player_3, 15))
    edges.append(Edge(node_player_2, node_player_3, 6))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph

@pytest.fixture
def mcstEdges():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)

    mcst_edges = []
    mcst_edges.append(Edge(node_source_b, node_player_1, 3))
    mcst_edges.append(Edge(node_source_b, node_player_3, 5))
    mcst_edges.append(Edge(node_player_2, node_player_3, 6))
    mcst_edges.append(Edge(node_source_a, node_player_3, 7))
    return mcst_edges

@pytest.fixture
def edges_not_in_mcst():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)

    not_mcst_edges = []
    not_mcst_edges.append(Edge(node_source_a, node_source_b, 12))
    not_mcst_edges.append(Edge(node_source_a, node_player_1, 11))
    not_mcst_edges.append(Edge(node_source_a, node_player_2, 8))
    not_mcst_edges.append(Edge(node_source_b, node_player_2, 9))
    not_mcst_edges.append(Edge(node_player_1, node_player_2, 13))
    not_mcst_edges.append(Edge(node_player_1, node_player_3, 15))
    return not_mcst_edges

def test_get_max_cost_on_path_one_max():
    rr = RegularReduce()
    path = []
    path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=2))
    path.append(Edge(Node(label=1), Node(label=2), cost=7))
    path.append(Edge(Node(type='source', label='a'), Node(label=3), cost=4))
    assert rr.get_max_cost_on_path(path) == 7

def test_get_max_cost_on_path_all_max():
    rr = RegularReduce()
    path = []
    path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    path.append(Edge(Node(label=1), Node(label=2), cost=7))
    path.append(Edge(Node(type='source', label='a'), Node(label=3), cost=7))
    assert rr.get_max_cost_on_path(path) == 7

def test_get_max_cost_on_path_last_max():
    rr = RegularReduce()
    path = []
    path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=2))
    path.append(Edge(Node(label=1), Node(label=2), cost=7))
    path.append(Edge(Node(type='source', label='a'), Node(label=3), cost=9))
    assert rr.get_max_cost_on_path(path) == 9

def test_get_max_cost_on_path_first_max():
    rr = RegularReduce()
    path = []
    path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=21))
    path.append(Edge(Node(label=1), Node(label=2), cost=7))
    path.append(Edge(Node(type='source', label='a'), Node(label=3), cost=9))
    assert rr.get_max_cost_on_path(path) == 21

def test_get_edges_not_in_mcst(graph:Graph, mcstEdges:list[Edge], edges_not_in_mcst:list[Edge]):
    edges_not_in_mcst_str = []
    for edge in edges_not_in_mcst:
        edges_not_in_mcst_str.append(edge.to_string())
    rr = RegularReduce(graph=graph, mcst_edges=mcstEdges)
    edges_not_in_mcst_rr = rr.get_edges_not_in_mcst()
    for edge in edges_not_in_mcst_rr:
        assert edge.to_string() in edges_not_in_mcst_str
    