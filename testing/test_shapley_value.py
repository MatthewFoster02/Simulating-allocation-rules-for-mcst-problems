import pytest

from graph.graph import Graph
from graph.edge import Edge
from graph.node import Node
from cooperative_functions.shapley_value import ShapleyValue
from cooperative_functions.cooperative_gt import CoopMethods
from irreducibililty.regular_reduce import RegularReduce
from run_shapley_of_irreducible import get_random_source_sets

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
def coalitions_3_players():
    return {
        '1': 4,
        '2': 3,
        '3': 2,
        '12': 7,
        '13': 5,
        '23': 5,
        '123': 8
    }

@pytest.fixture
def coalitions_4_players():
    return {
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

def test_get_all_orderings_3_players():
    sv = ShapleyValue(num_players=3)
    orderings_expected = ['123', '132', '213', '231', '312', '321']
    assert sv.get_all_orderings() == orderings_expected

def test_get_all_orderings_4_players():
    sv = ShapleyValue(num_players=4)
    orderings_expected = ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314', '2341', '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', '4213', '4231', '4312', '4321']
    assert sv.get_all_orderings() == orderings_expected

def test_average_values():
    sv = ShapleyValue()
    input_lst = [[2, 3, 5], [3, 4, 2], [4, 2, 2]]
    assert sv.average_values(input_lst) == [3, 3, 3]

def test_average_values_3_players():
    sv = ShapleyValue()
    input_lst = [[4, 3, 1], [4, 3, 1], [4, 3, 1], [3, 3, 2], [3, 3, 2], [3, 3, 2]]
    assert sv.average_values(input_lst) == [3.5, 3, 1.5]

def test_get_value(coalitions_3_players:dict):
    sv = ShapleyValue(coalitions=coalitions_3_players, num_players=3)
    assert sv.get_value('123') == [4, 3, 1]

def test_get_value(coalitions_3_players:dict):
    sv = ShapleyValue(coalitions=coalitions_3_players, num_players=3)
    assert sv.get_value('231') == [3, 3, 2]

def test_get_shapley_value_3_players(coalitions_3_players:dict):
    sv = ShapleyValue(coalitions=coalitions_3_players, num_players=3)
    shapley_value = sv.get_shapley_value()
    assert shapley_value == [3.5, 3, 1.5]

def test_get_shapley_value_4_players(coalitions_4_players:dict):
    sv = ShapleyValue(coalitions=coalitions_4_players, num_players=4)
    shapley_value = sv.get_shapley_value()
    assert shapley_value == [8.75, 6.25, 2.25, 1.75]

def test_sort_order_in_order():
    sv = ShapleyValue()
    assert sv.sort_order('123') == '123'

def test_sort_order_different():
    sv = ShapleyValue()
    assert sv.sort_order('312') == '123'

def test_sort_order_in_reverse():
    sv = ShapleyValue()
    assert sv.sort_order('4321') == '1234'


# Testing reducing graph and shapley value
def test_reducing_and_shapley(graph:Graph, mcstEdges:list[Edge]):
    rr = RegularReduce(graph=graph, mcst_edges=mcstEdges)
    reduced_graph = rr.reduce_graph()

    coop = CoopMethods(graph=reduced_graph)
    coalitions = coop.get_player_coalition_values(source_a_set={1, 2}, source_b_set={2, 3})

    assert coalitions == {
        '1': 7,
        '2': 13,
        '3': 5,
        '12': 16,
        '13': 12,
        '23': 18,
        '123': 21
    }

    sv = ShapleyValue(coalitions=coalitions, num_players=3)
    shapley_value = sv.get_shapley_value()
    assert shapley_value == [5, 11, 5]

def test_random_source_sets():
    players = []
    players.append(Node(label=1))
    players.append(Node(label=2))
    players.append(Node(label=3))
    source_a_set, source_b_set = get_random_source_sets(players=players)
    assert len(source_a_set) + len(source_b_set) == 4
    assert len(source_a_set.union(source_b_set)) == 3
