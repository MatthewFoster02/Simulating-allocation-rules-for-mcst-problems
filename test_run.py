import pytest

import run
from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from mcst import MCST

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
def graph_1c():
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
def graph_2c():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 12))
    edges.append(Edge(node_source_a, node_player_1, 9))
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
def graph_breaking():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 17))
    edges.append(Edge(node_source_a, node_player_1, 4))
    edges.append(Edge(node_source_a, node_player_2, 12))
    edges.append(Edge(node_source_a, node_player_3, 19))
    edges.append(Edge(node_source_b, node_player_1, 13))
    edges.append(Edge(node_source_b, node_player_2, 19))
    edges.append(Edge(node_source_b, node_player_3, 10))
    edges.append(Edge(node_player_1, node_player_2, 11))
    edges.append(Edge(node_player_1, node_player_3, 1))
    edges.append(Edge(node_player_2, node_player_3, 7))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph

def test_generate_source_sets_3():
    players = [Node(label=1), Node(label=2), Node(label=3)]
    source_a_set, source_b_set = run.get_random_source_sets(players)
    assert 1 <= len(source_a_set) <= 2
    assert 1 <= len(source_b_set) <= 2
    assert source_a_set.union(source_b_set) == {1, 2, 3}

def test_generate_source_sets_4():
    players = [Node(label=1), Node(label=2), Node(label=3), Node(label=4)]
    source_a_set, source_b_set = run.get_random_source_sets(players)
    assert 1 <= len(source_a_set) <= 3
    assert 1 <= len(source_b_set) <= 3
    assert source_a_set.union(source_b_set) == {1, 2, 3, 4}

def test_get_mcst_cost_subgraph(graph:Graph):
    source_a_set = {1, 2}
    source_b_set = {3}
    subgraph_a_cost = run.get_mcst_cost_subgraph(graph=graph, source_set=source_a_set, source='a')
    subgraph_b_cost = run.get_mcst_cost_subgraph(graph=graph, source_set=source_b_set, source='b')
    assert subgraph_a_cost == 18
    assert subgraph_b_cost == 5

def test_will_optimal_solution_hace_2_components_true(graph_2c:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    mcst = MCST(graph=graph_2c, source_a_set=source_a_set, source_b_set=source_b_set)

    assert run.will_optimal_solution_have_2_components(mcst, graph_2c, source_a_set, source_b_set)

def test_will_optimal_solution_hace_2_components_false(graph_1c:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    mcst = MCST(graph=graph_1c, source_a_set=source_a_set, source_b_set=source_b_set)

    assert not run.will_optimal_solution_have_2_components(mcst, graph_1c, source_a_set, source_b_set)

def test_breaking_example(graph_breaking:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    mcst = MCST(graph=graph_breaking, source_a_set=source_a_set, source_b_set=source_b_set)

    assert run.will_optimal_solution_have_2_components(mcst, graph_breaking, source_a_set, source_b_set)
