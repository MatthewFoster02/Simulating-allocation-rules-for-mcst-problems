import pytest

from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from cooperative_gt import CoopMethods
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
def graph_thesis():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 2))
    edges.append(Edge(node_source_a, node_player_1, 9))
    edges.append(Edge(node_source_a, node_player_2, 8))
    edges.append(Edge(node_source_a, node_player_3, 7))
    edges.append(Edge(node_source_b, node_player_1, 4))
    edges.append(Edge(node_source_b, node_player_2, 3))
    edges.append(Edge(node_source_b, node_player_3, 8))
    edges.append(Edge(node_player_1, node_player_2, 5))
    edges.append(Edge(node_player_1, node_player_3, 6))
    edges.append(Edge(node_player_2, node_player_3, 4))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph

@pytest.fixture
def graph4():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    node_player_4 = Node(label=4)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 12))
    edges.append(Edge(node_source_a, node_player_1, 10))
    edges.append(Edge(node_source_a, node_player_2, 8))
    edges.append(Edge(node_source_a, node_player_3, 7))
    edges.append(Edge(node_source_a, node_player_4, 3))
    edges.append(Edge(node_source_b, node_player_1, 3))
    edges.append(Edge(node_source_b, node_player_2, 9))
    edges.append(Edge(node_source_b, node_player_3, 5))
    edges.append(Edge(node_source_b, node_player_4, 16))
    edges.append(Edge(node_player_1, node_player_2, 13))
    edges.append(Edge(node_player_1, node_player_3, 15))
    edges.append(Edge(node_player_1, node_player_4, 17))
    edges.append(Edge(node_player_2, node_player_3, 6))
    edges.append(Edge(node_player_2, node_player_4, 2))
    edges.append(Edge(node_player_3, node_player_4, 9))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3, node_player_4]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph


def test_get_edge_correct(graph:Graph):
    coop = CoopMethods(graph)
    first_node = 'a'
    second_node = 3
    edge = coop.getEdgeWithEndpoints(first_node, second_node)
    assert edge.to_string() == 'Node a is connected to 3 with cost of 7'

def test_get_edge_inverted(graph:Graph):
    coop = CoopMethods(graph)
    first_node = 3
    second_node = 'a'
    edge = coop.getEdgeWithEndpoints(first_node, second_node)
    assert edge.to_string() == 'Node a is connected to 3 with cost of 7'

def test_get_edges_between_one(graph:Graph):
    coop = CoopMethods(graph)
    players = [1]
    source = 'a'
    edges = coop.getEdgesBetweenPlayersAndSource(players, source)
    assert edges[0].to_string() == 'Node a is connected to 1 with cost of 10'

def test_get_edges_between_two(graph:Graph):
    coop = CoopMethods(graph)
    players = [1, 3]
    source = 'a'
    edges = coop.getEdgesBetweenPlayersAndSource(players, source)
    assert edges[0].to_string() == 'Node a is connected to 1 with cost of 10'
    assert edges[1].to_string() == 'Node a is connected to 3 with cost of 7'

def test_get_edge_between_sources(graph:Graph):
    coop = CoopMethods(graph)
    edge = coop.getEdgeBetweenSources()
    assert edge.to_string() == 'Node a is connected to b with cost of 12'

def test_coalition_values_3_players(graph:Graph):
    coop = CoopMethods(graph)
    source_set_a = {1}
    source_set_b = {2, 3}
    coaltitions = coop.get_player_coalition_values(source_set_a, source_set_b)
    assert coaltitions == {
        '1': 10,
        '2': 9,
        '3': 5,
        '12': 19,
        '13': 15,
        '23': 11,
        '123': 21
    }

def test_coalition_values_3_players_thesis(graph_thesis:Graph):
    coop = CoopMethods(graph_thesis)
    source_set_a = {2, 3}
    source_set_b = {1}
    coaltitions = coop.get_player_coalition_values(source_set_a, source_set_b)
    assert coaltitions == {
        '1': 4,
        '2': 8,
        '3': 7,
        '12': 9,
        '13': 11,
        '23': 11,
        '123': 13
    }

def test_coalition_values_4_players(graph4:Graph):
    coop = CoopMethods(graph4)
    source_set_a = {1, 4}
    source_set_b = {2, 3}
    coaltitions = coop.get_player_coalition_values(source_set_a, source_set_b)
    assert coaltitions == {
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
    }

def test_allocation_in_core_3_players():
    coop = CoopMethods()
    coalitions = {
        '1': 10,
        '2': 9,
        '3': 5,
        '12': 19,
        '13': 15,
        '23': 11,
        '123': 21
    }

    allocation = [10, 6, 5]
    assert coop.belongs_to_core(coalitions, allocation)

def test_allocation_in_core_4_players():
    coop = CoopMethods()
    coalitions = {
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
    }

    allocation = [6, 6, 4, 3]
    assert coop.belongs_to_core(coalitions, allocation)

def test_allocation_not_in_core_3_players():
    coop = CoopMethods()
    coalitions = {
        '1': 10,
        '2': 9,
        '3': 5,
        '12': 19,
        '13': 15,
        '23': 11,
        '123': 21
    }

    allocation = [5, 5, 11]
    assert not coop.belongs_to_core(coalitions, allocation)

def test_allocation_not_in_core_4_players():
    coop = CoopMethods()
    coalitions = {
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
    }

    allocation = [3, 3, 7, 6]
    assert not coop.belongs_to_core(coalitions, allocation)

def test_allocation_in_core_3_players_int():
    coop = CoopMethods()
    coalitions = {
        '1': 20,
        '2': 11,
        '3': 11,
        '12': 26,
        '13': 31,
        '23': 22,
        '123': 36
    }

    allocation = [19.16667, 6.16666, 10.66666]
    assert coop.belongs_to_core(coalitions, allocation)

def test_allocation_in_core_3_players_thesis():
    coop = CoopMethods()
    coalitions = {
        '1': 4,
        '2': 3,
        '3': 6,
        '12': 7,
        '13': 10,
        '23': 6,
        '123': 10
    }

    allocation = [4, 3, 3]
    assert coop.belongs_to_core(coalitions, allocation)
