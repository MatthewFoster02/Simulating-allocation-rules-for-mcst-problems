import pytest

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
    return MCST(graph=graph)

@pytest.fixture
def sortedEdges():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)

    sorted_edges = []
    sorted_edges.append(Edge(node_source_b, node_player_1, 3))
    sorted_edges.append(Edge(node_source_b, node_player_3, 5))
    sorted_edges.append(Edge(node_player_2, node_player_3, 6))
    sorted_edges.append(Edge(node_source_a, node_player_3, 7))
    sorted_edges.append(Edge(node_source_a, node_player_2, 8))
    sorted_edges.append(Edge(node_source_b, node_player_2, 9))
    sorted_edges.append(Edge(node_source_a, node_player_1, 10))
    sorted_edges.append(Edge(node_source_a, node_source_b, 12))
    sorted_edges.append(Edge(node_player_1, node_player_2, 13))
    sorted_edges.append(Edge(node_player_1, node_player_3, 15))
    return sorted_edges

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

def test_sort_edges_by_cost(graph:MCST, sortedEdges:list[Edge]):
    edges_sorted = graph.getEdges()
    edges_sorted_str = ''
    sortedEdgesStr = ''
    for edge1, edge2 in zip(edges_sorted, sortedEdges):
        edges_sorted_str += edge1.to_string()
        sortedEdgesStr += edge2.to_string()
    assert edges_sorted_str == sortedEdgesStr

def test_mcst_solution(graph:MCST, mcstEdges:list[Edge]):
    expectedTotalCost = 21
    mcst_edges, total_cost = graph.kruskal()
    mcst_edges_str = ''
    mcstEdgesStr = ''
    for edge1, edge2 in zip(mcst_edges, mcstEdges):
        mcst_edges_str += edge1.to_string()
        mcstEdgesStr += edge2.to_string()
    assert mcst_edges_str == mcstEdgesStr
    assert total_cost == expectedTotalCost

def test_cycle_created_true(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2, 3}]
    edgeToAdd = Edge(Node(label=1), Node(label=3), 10)
    graph.setSets(currentStates)
    assert graph.is_cycle_created(edgeToAdd)

def test_cycle_created_false(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    edgeToAdd = Edge(Node(label=1), Node(label=3), 10)
    graph.setSets(currentStates)
    assert not graph.is_cycle_created(edgeToAdd)

def test_find_sets_different_sets(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    graph.setSets(currentStates)
    node_u_label = 'a'
    node_v_label = 1
    node_u_set, node_v_set = graph.find_sets(node_u_label, node_v_label)
    assert not node_u_set == node_v_set
    assert node_u_set == {'a'}
    assert node_v_set == {1, 2}

def test_find_sets_same_sets(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    graph.setSets(currentStates)
    node_u_label = 2
    node_v_label = 1
    node_u_set, node_v_set = graph.find_sets(node_u_label, node_v_label)
    assert node_u_set == node_v_set == {1, 2}

def test_join_sets_different_sets(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    graph.setSets(currentStates)
    node_u_set = {'a'}
    node_v_set = {3}
    graph.join_sets(node_u_set, node_v_set)
    updatedStates = graph.getSets()
    assert updatedStates == [{'b'}, {1, 2}, {'a', 3}]

def test_join_sets_same_set(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    graph.setSets(currentStates)
    node_u_set = {1, 2}
    node_v_set = {1, 2}
    graph.join_sets(node_u_set, node_v_set)
    updatedStates = graph.getSets()
    assert updatedStates == [{'a'}, {'b'}, {3}, {1, 2}]

def test_share_cost_evenly_one_player(graph:MCST):
    cost = 3
    component_sharing = {1}
    graph.share_evenly(component_sharing, cost)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [3, 0, 0]

def test_share_cost_evenly_multiple_players(graph:MCST):
    cost = 4.5
    component_sharing = {1, 2, 3}
    graph.share_evenly(component_sharing, cost)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [1.5, 1.5, 1.5]

def test_share_proportionately(graph:MCST):
    cost = 5
    component_sharing1 = {1, 2}
    component_sharing2 = {3}
    graph.share_proportionately(component_sharing1, component_sharing2, cost)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [1.25, 1.25, 2.5]

def test_check_disconnted_one(graph:MCST, mcstEdges:list[Edge]):
    graph.setEdges(mcstEdges)
    graph.setSourceASet({3})
    graph.setSourceBSet({1, 2})
    graph.remove_check_disconnected(graph.getEdges()[-1], 5)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 0, 5]

def test_check_disconnted_multiple(graph:MCST, mcstEdges:list[Edge]):
    graph.setEdges(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.remove_check_disconnected(graph.getEdges()[-1], 5)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 2.5, 2.5]

def test_check_disconnted_none(graph:MCST, mcstEdges:list[Edge]):
    graph.setEdges(mcstEdges)
    graph.setSourceASet(set())
    graph.setSourceBSet({1, 2, 3})
    graph.remove_check_disconnected(graph.getEdges()[-1], 5)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 0, 0]
