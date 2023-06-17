import pytest

from cooperative_functions.cooperative_gt import CoopMethods
from irreducibililty.fix_over_reduce import FixOverReduce
from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph

@pytest.fixture
def original_graph():
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
def reduced_graph():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 2))
    edges.append(Edge(node_source_a, node_player_1, 4))
    edges.append(Edge(node_source_a, node_player_2, 3))
    edges.append(Edge(node_source_a, node_player_3, 4))
    edges.append(Edge(node_source_b, node_player_1, 4))
    edges.append(Edge(node_source_b, node_player_2, 3))
    edges.append(Edge(node_source_b, node_player_3, 4))
    edges.append(Edge(node_player_1, node_player_2, 4))
    edges.append(Edge(node_player_1, node_player_3, 4))
    edges.append(Edge(node_player_2, node_player_3, 4))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph

@pytest.fixture
def reduced_graph_one_component():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 2))
    edges.append(Edge(node_source_a, node_player_1, 9))
    edges.append(Edge(node_source_a, node_player_2, 5))
    edges.append(Edge(node_source_a, node_player_3, 5))
    edges.append(Edge(node_source_b, node_player_1, 4))
    edges.append(Edge(node_source_b, node_player_2, 3))
    edges.append(Edge(node_source_b, node_player_3, 4))
    edges.append(Edge(node_player_1, node_player_2, 4))
    edges.append(Edge(node_player_1, node_player_3, 4))
    edges.append(Edge(node_player_2, node_player_3, 4))

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
    mcst_edges.append(Edge(node_source_a, node_source_b, 2))
    mcst_edges.append(Edge(node_source_b, node_player_2, 3))
    mcst_edges.append(Edge(node_source_b, node_player_1, 4))
    mcst_edges.append(Edge(node_player_2, node_player_3, 4))
    return mcst_edges

def test_is_over_reduced(reduced_graph:Graph, original_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}

    coop = CoopMethods(graph=original_graph)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)

    fixOverReduce = FixOverReduce(reduced_graph=reduced_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fixOverReduce.is_over_reduced(graph=reduced_graph)

def test_is_over_reduced_not(reduced_graph:Graph, original_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}

    coop = CoopMethods(graph=original_graph)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)

    fixOverReduce = FixOverReduce(reduced_graph=original_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert not fixOverReduce.is_over_reduced(graph=original_graph)

def test_get_cost_of_path(mcstEdges:list[Edge]):
    fix = FixOverReduce()
    assert fix.get_cost_of_path(mcstEdges) == 13

def test_find_cost_in_mcst_to_source_player1(mcstEdges:list[Edge]):
    source_a_set = {2, 3}
    source_b_set = {1}
    fix = FixOverReduce(mcst_edges=mcstEdges, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.find_cost_in_mcst_to_source(1) == 4

def test_find_cost_in_mcst_to_source_player2(mcstEdges:list[Edge]):
    source_a_set = {2, 3}
    source_b_set = {1}
    fix = FixOverReduce(mcst_edges=mcstEdges, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.find_cost_in_mcst_to_source(2) == 5

def test_find_cost_in_mcst_to_source_player3(mcstEdges:list[Edge]):
    source_a_set = {2, 3}
    source_b_set = {1}
    fix = FixOverReduce(mcst_edges=mcstEdges, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.find_cost_in_mcst_to_source(3) == 9

def test_get_all_edges_with_endpoints_one(original_graph:Graph):
    fix = FixOverReduce(reduced_graph=original_graph)
    endpoints = ['b', 1]
    edges = fix.get_all_edges_with_endpoints(endpoints=endpoints)
    assert edges[0].to_string() == 'Node b is connected to 1 with cost of 4' 

def test_get_all_edges_with_endpoints_three(original_graph:Graph):
    fix = FixOverReduce(reduced_graph=original_graph)
    endpoints = ['a', 2, 3]
    edges = fix.get_all_edges_with_endpoints(endpoints=endpoints)
    for edge in edges:
        assert  edge.to_string() == 'Node a is connected to 2 with cost of 8' or \
                edge.to_string() == 'Node a is connected to 3 with cost of 7' or \
                edge.to_string() == 'Node 2 is connected to 3 with cost of 4'

def test_get_edges_between_players_and_source(original_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    fix = FixOverReduce(reduced_graph=original_graph, source_a_set=source_a_set, source_b_set=source_b_set)
    edges = fix.get_edges_between_players_and_source(source_label='a')
    for edge in edges:
        assert  edge.to_string() == 'Node a is connected to 2 with cost of 8' or \
                edge.to_string() == 'Node a is connected to 3 with cost of 7' or \
                edge.to_string() == 'Node 2 is connected to 3 with cost of 4'

def test_is_edge_in_mcst(mcstEdges:list[Edge]):
    fix = FixOverReduce(mcst_edges=mcstEdges)
    edge = Edge(Node(label=2), Node(label=3), cost=4)
    assert fix.edge_in_mcst(edge=edge)

def test_is_edge_in_mcst_not(mcstEdges:list[Edge]):
    fix = FixOverReduce(mcst_edges=mcstEdges)
    edge = Edge(Node(type='source', label='a'), Node(label=2), cost=4)
    assert not fix.edge_in_mcst(edge=edge)

def test_does_reducing_change_grand_coalition(reduced_graph_one_component:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    coop = CoopMethods(graph=reduced_graph_one_component)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
    fix = FixOverReduce(original_graph=reduced_graph_one_component, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert reduced_graph_one_component.get_edges()[8].get_cost() == 5
    assert fix.does_reducing_change_grand_coalition(edge=reduced_graph_one_component.get_edges()[8])
    assert reduced_graph_one_component.get_edges()[8].get_cost() == 5

def test_does_reducing_change_grand_coalition_doesnt(reduced_graph_one_component:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    coop = CoopMethods(graph=reduced_graph_one_component)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
    fix = FixOverReduce(original_graph=reduced_graph_one_component, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert reduced_graph_one_component.get_edges()[9].get_cost() == 9
    assert not fix.does_reducing_change_grand_coalition(edge=reduced_graph_one_component.get_edges()[9])
    assert reduced_graph_one_component.get_edges()[9].get_cost() == 9

def test_is_at_lower_bound(reduced_graph:Graph):
    edge = Edge(Node(type='source', label='a'), Node(label=2), cost=3)
    fix = FixOverReduce(reduced_graph=reduced_graph)
    assert fix.is_edge_at_lower_bound(edge=edge)

def test_not_at_lower_bound(reduced_graph:Graph):
    edge = Edge(Node(type='source', label='a'), Node(label=2), cost=4)
    fix = FixOverReduce(reduced_graph=reduced_graph)
    assert not fix.is_edge_at_lower_bound(edge=edge)

def test_edge_no_further_reduce_2_comps(reduced_graph_one_component:Graph, reduced_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    coop = CoopMethods(graph=reduced_graph_one_component)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
    fix = FixOverReduce(original_graph=reduced_graph_one_component, reduced_graph=reduced_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.no_further_reduce(edge=reduced_graph_one_component.get_edges()[8])

def test_edge_no_further_reduce_lower_bound(reduced_graph:Graph, reduced_graph_one_component:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    coop = CoopMethods(graph=reduced_graph_one_component)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
    edge = Edge(Node(type='source', label='a'), Node(label=2), cost=3)
    fix = FixOverReduce(original_graph=reduced_graph_one_component, reduced_graph=reduced_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.no_further_reduce(edge=edge)

def test_edge_no_further_reduce_false(reduced_graph_one_component:Graph, reduced_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}
    coop = CoopMethods(graph=reduced_graph_one_component)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)
    fix = FixOverReduce(original_graph=reduced_graph_one_component, reduced_graph=reduced_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert not fix.no_further_reduce(edge=reduced_graph_one_component.get_edges()[9])

def test_entire_run(reduced_graph:Graph, mcstEdges:list[Node], original_graph:Graph):
    source_a_set = {2, 3}
    source_b_set = {1}

    coop = CoopMethods(graph=original_graph)
    original_coalitions = coop.get_player_coalition_values(source_a_set=source_a_set, source_b_set=source_b_set)

    fix = FixOverReduce(reduced_graph=reduced_graph, mcst_edges=mcstEdges, original_graph=original_graph, original_coalitions=original_coalitions, source_a_set=source_a_set, source_b_set=source_b_set)
    assert fix.is_over_reduced(reduced_graph)

    fixed_graph = fix.fix_over_reduce()
    assert not fix.is_over_reduced(fixed_graph)

    for edge in fixed_graph.get_edges():
        assert  edge.to_string() == 'Node a is connected to b with cost of 2' or \
                edge.to_string() == 'Node a is connected to 1 with cost of 4' or \
                edge.to_string() == 'Node a is connected to 2 with cost of 5' or \
                edge.to_string() == 'Node a is connected to 3 with cost of 5' or \
                edge.to_string() == 'Node b is connected to 1 with cost of 4' or \
                edge.to_string() == 'Node b is connected to 2 with cost of 3' or \
                edge.to_string() == 'Node b is connected to 3 with cost of 4' or \
                edge.to_string() == 'Node 1 is connected to 2 with cost of 4' or \
                edge.to_string() == 'Node 1 is connected to 3 with cost of 4' or \
                edge.to_string() == 'Node 2 is connected to 3 with cost of 4'
