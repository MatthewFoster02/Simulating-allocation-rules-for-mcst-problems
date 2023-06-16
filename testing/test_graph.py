import pytest

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
    edges.append(Edge(node_source_a, node_player_1, 10))
    edges.append(Edge(node_source_a, node_player_2, 8))
    edges.append(Edge(node_source_b, node_player_1, 3))
    edges.append(Edge(node_source_b, node_player_2, 9))
    edges.append(Edge(node_player_1, node_player_2, 13))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    return Graph(edges=edges, sources=sources, players=players)

@pytest.fixture
def graphConnected():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_b, node_player_1, 3))
    edges.append(Edge(node_source_b, node_player_3, 5))
    edges.append(Edge(node_player_2, node_player_3, 6))
    edges.append(Edge(node_source_a, node_player_3, 7))
    edges.append(Edge(node_source_a, node_player_2, 8))
    edges.append(Edge(node_source_b, node_player_2, 9))
    edges.append(Edge(node_source_a, node_player_1, 10))
    edges.append(Edge(node_source_a, node_source_b, 12))
    edges.append(Edge(node_player_1, node_player_2, 13))
    edges.append(Edge(node_player_1, node_player_3, 15))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    return Graph(edges=edges, sources=sources, players=players)

def test_path_between_exists_true(graph:Graph):
    node_u_label = 1
    node_v_label = 'a'
    assert graph.check_path_between_2_nodes(node_u_label, node_v_label)

def test_path_between_exists_false(graph:Graph):
    node_u_label = 3
    node_v_label = 'a'
    assert not graph.check_path_between_2_nodes(node_u_label, node_v_label)

def test_edges_equal_true():
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    edge1 = Edge(node_source_b, node_player_1, 3)
    edge2 = Edge(node_source_b, node_player_1, 3)
    assert edge1.is_same_edge_excluding_cost(edge2)

def test_edges_equal_true_different_costs():
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    edge1 = Edge(node_source_b, node_player_1, 3)
    edge2 = Edge(node_source_b, node_player_1, 7)
    assert edge1.is_same_edge_excluding_cost(edge2)

def test_edges_equal_false():
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    edge1 = Edge(node_source_b, node_player_1, 3)
    edge2 = Edge(node_source_b, node_player_2, 3)
    assert not edge1.is_same_edge_excluding_cost(edge2)

def test_reduce_edge_cost():
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    edge = Edge(node_source_b, node_player_1, 3)
    edge.reduce_cost()
    assert edge.get_cost() == 2