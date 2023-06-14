import pytest

import run
import run_folk_rule_2_component_solutions
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

@pytest.fixture
def graph_breaking_2():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 15))
    edges.append(Edge(node_source_a, node_player_1, 15))
    edges.append(Edge(node_source_a, node_player_2, 13))
    edges.append(Edge(node_source_a, node_player_3, 14))
    edges.append(Edge(node_source_b, node_player_1, 16))
    edges.append(Edge(node_source_b, node_player_2, 6))
    edges.append(Edge(node_source_b, node_player_3, 2))
    edges.append(Edge(node_player_1, node_player_2, 16))
    edges.append(Edge(node_player_1, node_player_3, 4))
    edges.append(Edge(node_player_2, node_player_3, 4))

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

def test_breaking_example_2(graph_breaking_2:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    mcst = MCST(graph=graph_breaking_2, source_a_set=source_a_set, source_b_set=source_b_set)

    assert run.will_optimal_solution_have_2_components(mcst, graph_breaking_2, source_a_set, source_b_set)

def test_combining_allocations_3_players():
    source_a_set = {2, 3}
    source_b_set = {1}
    allocation_a = [3, 6]
    allocation_b = [9]
    combined_allocation = run_folk_rule_2_component_solutions.join_sub_allocations(allocation_a, allocation_b, source_a_set, source_b_set)
    assert combined_allocation == [9, 3, 6]

def test_combining_allocations_4_players():
    source_a_set = {2, 3}
    source_b_set = {1, 4}
    allocation_a = [3, 6]
    allocation_b = [9, 21]
    combined_allocation = run_folk_rule_2_component_solutions.join_sub_allocations(allocation_a, allocation_b, source_a_set, source_b_set)
    assert combined_allocation == [9, 3, 6, 21]

def test_getting_subgraph_source_a(graph:Graph):
    source_a_set = {1, 2}
    subgraph_a = run_folk_rule_2_component_solutions.get_subgraph(graph=graph, source_set=source_a_set, source_label='a')
    sources = subgraph_a.get_sources()
    players = subgraph_a.get_players()

    expected_subgraph_edges = []
    expected_subgraph_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=10))
    expected_subgraph_edges.append(Edge(Node(type='source', label='a'), Node(label=2), cost=8))
    expected_subgraph_edges.append(Edge(Node(label=1), Node(label=2), cost=13))

    assert sources[0].to_string() == 'Label: a Type: source'
    for player in players:
        assert player.to_string() == 'Label: 1 Type: player' or player.to_string() == 'Label: 2 Type: player'
    
    subgraph_a_edges_str = ''
    expected_subgraph_edges_str = ''
    for edge1, edge2 in zip(subgraph_a.get_edges(), expected_subgraph_edges):
        subgraph_a_edges_str += edge1.to_string()
        expected_subgraph_edges_str += edge2.to_string()
    assert subgraph_a_edges_str == expected_subgraph_edges_str

def test_getting_subgraph_source_b(graph:Graph):
    source_b_set = {3}
    subgraph_b = run_folk_rule_2_component_solutions.get_subgraph(graph=graph, source_set=source_b_set, source_label='b')
    sources = subgraph_b.get_sources()
    players = subgraph_b.get_players()

    expected_subgraph_edges = []
    expected_subgraph_edges.append(Edge(Node(type='source', label='b'), Node(label=3), cost=5))

    assert sources[0].to_string() == 'Label: b Type: source'
    assert players[0].to_string() == 'Label: 3 Type: player'
    
    subgraph_b_edges_str = ''
    expected_subgraph_edges_str = ''
    for edge1, edge2 in zip(subgraph_b.get_edges(), expected_subgraph_edges):
        subgraph_b_edges_str += edge1.to_string()
        expected_subgraph_edges_str += edge2.to_string()
    assert subgraph_b_edges_str == expected_subgraph_edges_str

def test_getting_subgraph_source_b_2_players(graph:Graph):
    source_b_set = {2, 3}
    subgraph_b = run_folk_rule_2_component_solutions.get_subgraph(graph=graph, source_set=source_b_set, source_label='b')
    sources = subgraph_b.get_sources()
    players = subgraph_b.get_players()

    expected_subgraph_edges = []
    expected_subgraph_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))
    expected_subgraph_edges.append(Edge(Node(type='source', label='b'), Node(label=3), cost=5))
    expected_subgraph_edges.append(Edge(Node(label=2), Node(label=3), cost=6))

    assert sources[0].to_string() == 'Label: b Type: source'
    for player in players:
        assert player.to_string() == 'Label: 2 Type: player' or player.to_string() == 'Label: 3 Type: player'
    
    subgraph_b_edges_str = ''
    expected_subgraph_edges_str = ''
    for edge1, edge2 in zip(subgraph_b.get_edges(), expected_subgraph_edges):
        subgraph_b_edges_str += edge1.to_string()
        expected_subgraph_edges_str += edge2.to_string()
    assert subgraph_b_edges_str == expected_subgraph_edges_str

def test_run_a_4():
    graph_a_coalitions = {'4': 20}
    graph_b_coalitions = {'1': 4, '2': 20, '3': 12}
    num = run_folk_rule_2_component_solutions.test_coalition_checker(graph_a_coalitions, graph_b_coalitions)
    assert num == 0

def test_run_b_4():
    graph_a_coalitions = {'1': 4, '2': 20, '3': 12}
    graph_b_coalitions = {'4': 20}
    num = run_folk_rule_2_component_solutions.test_coalition_checker(graph_a_coalitions, graph_b_coalitions)
    assert num == 1

def test_run_neither_4():
    graph_a_coalitions = {'3': 12, '4': 20}
    graph_b_coalitions = {'1': 4, '2': 20}
    num = run_folk_rule_2_component_solutions.test_coalition_checker(graph_a_coalitions, graph_b_coalitions)
    assert num == 2
