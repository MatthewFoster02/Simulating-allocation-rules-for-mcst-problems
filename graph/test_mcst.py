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
    sorted_edges.append(Edge(node_source_a, node_player_1, 11))
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

def test_join_sets_different_sets_in_order(graph:MCST):
    currentStates = [{1}, {2}, {3}, {'a'}]
    graph.setSets(currentStates)
    node_u_set = {1}
    node_v_set = {2}
    graph.join_sets(node_u_set, node_v_set)
    updatedStates = graph.getSets()
    assert set(frozenset(s) for s in updatedStates) == {frozenset({3}), frozenset({'a'}), frozenset({1, 2})}

def test_join_sets_same_set(graph:MCST):
    currentStates = [{'a'}, {'b'}, {1, 2}, {3}]
    graph.setSets(currentStates)
    node_u_set = {1, 2}
    node_v_set = {1, 2}
    graph.join_sets(node_u_set, node_v_set)
    updatedStates = graph.getSets()
    assert set(frozenset(s) for s in updatedStates) == {frozenset({'a'}), frozenset({'b'}), frozenset({3}), frozenset({1, 2})}

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

def test_share_proportionately_same_size_components(graph:MCST):
    cost = 4
    component_sharing1 = {1}
    component_sharing2 = {2}
    graph.share_proportionately(component_sharing1, component_sharing2, cost)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [2, 2, 0]

def test_share_proportionately_different_size_components(graph:MCST):
    cost = 12
    component_sharing1 = {1, 2}
    component_sharing2 = {3}
    graph.share_proportionately(component_sharing1, component_sharing2, cost)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [2, 2, 8]

def test_check_disconnted_one(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({3})
    graph.setSourceBSet({1, 2})
    graph.remove_check_disconnected(graph.getMCST()[-1], 7)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 0, 7]

def test_check_disconnted_multiple(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.remove_check_disconnected(graph.getMCST()[-1], 7)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 3.5, 3.5]

def test_check_disconnted_none(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet(set())
    graph.setSourceBSet({1, 2, 3})
    graph.remove_check_disconnected(graph.getMCST()[-1], 7)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 0, 0]

def test_find_set_without_source_second_set_a(graph:MCST):
    first_set = {'a', 1, 2}
    second_set = {3}
    set_without_source, set_with_source = graph.find_set_without_source(first_set, second_set)
    assert set_without_source == second_set
    assert set_with_source == first_set

def test_find_set_without_source_second_set_b(graph:MCST):
    first_set = {'b', 1, 2}
    second_set = {3}
    set_without_source, set_with_source = graph.find_set_without_source(first_set, second_set)
    assert set_without_source == second_set
    assert set_with_source == first_set

def test_find_set_without_source_first_set_a(graph:MCST):
    first_set = {1, 2}
    second_set = {'a', 3}
    set_without_source, set_with_source = graph.find_set_without_source(first_set, second_set)
    assert set_without_source == first_set
    assert set_with_source == second_set

def test_find_set_without_source_first_set_b(graph:MCST):
    first_set = {1, 2}
    second_set = {'b', 3}
    set_without_source, set_with_source = graph.find_set_without_source(first_set, second_set)
    assert set_without_source == first_set
    assert set_with_source == second_set

def test_has_both_sources_true(graph:MCST):
    component = {'a', 'b', 1}
    assert graph.hasBothSources(component)

def test_has_both_sources_false_1(graph:MCST):
    component = {'a', 1, 2, 3}
    assert not graph.hasBothSources(component)

def test_has_both_sources_false_none(graph:MCST):
    component = {1, 2}
    assert not graph.hasBothSources(component)

def test_one_has_one_source_true_first(graph:MCST):
    first_set = {'b', 3}
    second_set = {1, 2}
    assert graph.oneHasOneSource(first_set, second_set)

def test_one_has_one_source_true_second(graph:MCST):
    first_set = {1, 2}
    second_set = {'a', 3}
    assert graph.oneHasOneSource(first_set, second_set)

def test_one_has_one_source_false_none(graph:MCST):
    first_set = {1, 2}
    second_set = {3}
    assert not graph.oneHasOneSource(first_set, second_set)

def test_one_has_one_source_false_first_both(graph:MCST):
    first_set = {'a', 'b', 1, 2}
    second_set = {3}
    assert not graph.oneHasOneSource(first_set, second_set)

def test_one_has_one_source_false_second_both(graph:MCST):
    first_set = {1, 2, 3}
    second_set = {'a', 'b'}
    assert not graph.oneHasOneSource(first_set, second_set)

def test_has_source_true_one(graph:MCST):
    component = {'a', 2, 3}
    assert graph.hasSource(component)

def test_has_source_true_both(graph:MCST):
    component = {'a', 'b', 2, 3}
    assert graph.hasSource(component)

def test_has_source_false(graph:MCST):
    component = {1, 2, 3}
    assert not graph.hasSource(component)

def test_joining_components_no_source(graph:MCST):
    sets_to_be = [{'a', 'b'}, {1, 2}, {3}]
    graph.setSets(sets_to_be)
    assert graph.determineJoiningComponents(2, 3) == 'nosource'

def test_joining_components_one_source(graph:MCST):
    sets_to_be = [{'a', 1}, {2, 3}, {'b'}]
    graph.setSets(sets_to_be)
    assert graph.determineJoiningComponents(1, 2) == 'onesource'

def test_joining_components_both_sources(graph:MCST):
    sets_to_be = [{'a', 1}, {2, 3}, {'b'}]
    graph.setSets(sets_to_be)
    assert graph.determineJoiningComponents(1, 'b') == 'bothsources'

def test_joining_components_2_sources(graph:MCST):
    sets_to_be = [{'a', 'b', 1}, {2, 3}]
    graph.setSets(sets_to_be)
    assert graph.determineJoiningComponents('a', 3) == '2sources'

def test_has_this_source_true_a(graph:MCST):
    component = {'a', 'b', 2}
    assert graph.has_this_source(component, {'a'})

def test_has_this_source_true_b(graph:MCST):
    component = {'b', 2, 3}
    assert graph.has_this_source(component, {'b'})

def test_has_this_source_false_a(graph:MCST):
    component = {1, 2, 3}
    assert not graph.has_this_source(component, {'a'})

def test_has_this_source_false_b(graph:MCST):
    component = {1, 2, 3}
    assert not graph.has_this_source(component, {'b'})

def test_check_benefiting_all_want_a(graph:MCST):
    check_set = {1, 2}
    other_set = {'a', 3}
    graph.setSourceASet({1, 2})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == {1, 2}

def test_check_benefiting_all_want_b(graph:MCST):
    check_set = {1, 2}
    other_set = {'b', 3}
    graph.setSourceBSet({1, 2})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == {1, 2}

def test_check_benefiting_subset_want_a(graph:MCST):
    check_set = {1, 2, 3}
    other_set = {'a'}
    graph.setSourceASet({2, 3})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == {2, 3}

def test_check_benefiting_subset_want_b(graph:MCST):
    check_set = {1, 2, 3}
    other_set = {'b'}
    graph.setSourceBSet({2})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == {2}

def test_check_benefiting_all_both(graph:MCST):
    check_set = {1, 2, 3}
    other_set = {'a', 'b'}
    graph.setSourceBSet({2})
    graph.setSourceASet({1, 3})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == {1, 2, 3}

def test_check_benefiting_none_players(graph:MCST):
    check_set = {1, 2, 3}
    other_set = {'a', 'b'}
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == set()

def test_check_benefiting_none_sources(graph:MCST):
    check_set = {'b'}
    other_set = {'a'}
    graph.setSourceBSet({2})
    graph.setSourceASet({1, 3})
    beneficiaries = graph.checkBenefiting(check_set, other_set)
    assert beneficiaries == set()

def test_share_edge_cost_no_source(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.setSets([{'a'}, {'b'}, {1, 2}, {3}])
    graph.share_cost_of_edge(Edge(Node(label=2), Node(label=3), 6))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [1, 1, 4]

def test_share_edge_cost_one_source_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.setSets([{'a', 1, 2}, {'b'}, {3}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 7))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 0, 7]

def test_share_edge_cost_one_source_different_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({1, 2})
    graph.setSourceBSet({3})
    graph.setSets([{'a'}, {'b'}, {1}, {2, 3}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 10))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 10, 0]

def test_share_edge_cost_one_source_no_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({1, 2})
    graph.setSourceBSet({3})
    graph.setSets([{'a'}, {'b'}, {1, 2}, {3}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 7))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [3.5, 3.5, 0]

def test_share_edge_cost_both_sources_no_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.setSets([{'a', 3}, {'b', 1}, {2}])
    graph.share_cost_of_edge(Edge(Node(label=2), Node(label=3), 6))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [0, 6, 0]

def test_share_edge_cost_both_sources_one_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2})
    graph.setSourceBSet({1, 3})
    graph.setSets([{'a', 1}, {'b', 3}, {2}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 7))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [7, 0, 0]

def test_share_edge_cost_both_sources_both_beneficiaries(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.setSets([{'a', 1}, {'b', 2, 3}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 9))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [6, 1.5, 1.5]

def test_share_edge_cost_2_sources(graph:MCST, mcstEdges:list[Edge]):
    graph.setMCST(mcstEdges)
    graph.setSourceASet({2, 3})
    graph.setSourceBSet({1})
    graph.setSets([{'a', 'b'}, {1, 2, 3}])
    graph.share_cost_of_edge(Edge(Node(type='source', label='a'), Node(label=3), 7))
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [7/3, 7/3, 7/3]

def test_kruskal_with_sharing(graph:MCST):
    graph.setSourceASet({1})
    graph.setSourceBSet({2, 3})
    _ = graph.kruskal()
    #graph.setMCST(mcst_edges) 
    graph.kruskal(share_edge_costs=True)
    cost_allocation = graph.getCostAllocation()
    assert cost_allocation == [10, 6, 5]

def test_generate_sets(graph:MCST):
    sets = graph.generate_sets()
    assert sets == [{'a'}, {'b'}, {1}, {2}, {3}]
