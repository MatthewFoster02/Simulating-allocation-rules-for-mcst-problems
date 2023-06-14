import pytest

from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from first_rule_and_prims.mcst import MCST
from path_rule.path_checking_rule import PathRule

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
def graph_check():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    
    edges = []
    edges.append(Edge(node_source_a, node_source_b, 16))
    edges.append(Edge(node_source_a, node_player_1, 15))
    edges.append(Edge(node_source_a, node_player_2, 12))
    edges.append(Edge(node_source_a, node_player_3, 20))
    edges.append(Edge(node_source_b, node_player_1, 14))
    edges.append(Edge(node_source_b, node_player_2, 4))
    edges.append(Edge(node_source_b, node_player_3, 12))
    edges.append(Edge(node_player_1, node_player_2, 17))
    edges.append(Edge(node_player_1, node_player_3, 1))
    edges.append(Edge(node_player_2, node_player_3, 10))

    sources = [node_source_a, node_source_b]
    players = [node_player_1, node_player_2, node_player_3]

    graph = Graph(edges=edges, sources=sources, players=players)
    return graph

@pytest.fixture
def mcstEdgesCheck():
    node_source_a = Node(type='source', label='a')
    node_source_b = Node(type='source', label='b')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)

    mcst_edges = []
    mcst_edges.append(Edge(node_player_1, node_player_3, 1))
    mcst_edges.append(Edge(node_source_b, node_player_2, 4))
    mcst_edges.append(Edge(node_player_2, node_player_3, 10))
    mcst_edges.append(Edge(node_source_a, node_player_2, 12))
    return mcst_edges

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

def test_get_individual_player_costs(graph:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    kruskal = MCST(graph=graph, source_a_set=source_a_set, source_b_set=source_b_set)
    mcst_edges, _ = kruskal.kruskal()
    pathRule = PathRule(graph=graph, mcst_edges=mcst_edges, source_a_set=source_a_set, source_b_set=source_b_set)
    pathRule.get_individual_player_costs()
    assert pathRule.get_individual_cost() == {
        '1': 1,
        '2': 9,
        '3': 5
    }

def test_get_path_cost():
    edges_in_path = []
    edges_in_path.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    edges_in_path.append(Edge(Node(label=1), Node(label=2), cost=4))
    edges_in_path.append(Edge(Node(type='source', label='b'), Node(label=2), cost=6))

    pathRule = PathRule()
    assert pathRule.get_path_cost(edges_in_path=edges_in_path) == 17

def test_get_wanted_source_a_true():
    source_a_set = {1}
    source_b_set = {2, 3}
    pathRule = PathRule(source_a_set=source_a_set, source_b_set=source_b_set)
    assert pathRule.get_wanted_source(1) == 'a'

def test_get_wanted_source_a_false():
    source_a_set = {1}
    source_b_set = {2, 3}
    pathRule = PathRule(source_a_set=source_a_set, source_b_set=source_b_set)
    assert not pathRule.get_wanted_source(3) == 'a'

def test_get_wanted_source_b_true():
    source_a_set = {1}
    source_b_set = {2, 3}
    pathRule = PathRule(source_a_set=source_a_set, source_b_set=source_b_set)
    assert pathRule.get_wanted_source(2) == 'b'

def test_get_wanted_source_b_false():
    source_a_set = {1}
    source_b_set = {2, 3}
    pathRule = PathRule(source_a_set=source_a_set, source_b_set=source_b_set)
    assert not pathRule.get_wanted_source(1) == 'b'

def test_get_path(mcstEdges:list[Edge]):
    pathRule = PathRule(mcst_edges=mcstEdges)
    path = pathRule.get_path(2, 'a')
    assert path[0].to_string() == 'Node a is connected to 3 with cost of 7'
    assert path[1].to_string() == 'Node 2 is connected to 3 with cost of 6'

def test_get_individual_player_costs(graph:Graph):
    source_a_set = {1}
    source_b_set = {2, 3}
    kruskal = MCST(graph=graph, source_a_set=source_a_set, source_b_set=source_b_set)
    mcst_edges, _ = kruskal.kruskal()
    pathRule = PathRule(graph=graph, mcst_edges=mcst_edges, source_a_set=source_a_set, source_b_set=source_b_set)
    pathRule.get_path_player_costs()
    assert pathRule.get_player_path_cost() == {
        '1': 15,
        '2': 11,
        '3': 5
    }
    player_path_edges = pathRule.get_player_path_edges()
    player1_path = player_path_edges['1']
    player2_path = player_path_edges['2']
    player3_path = player_path_edges['3']
    assert player1_path[0].to_string() == 'Node a is connected to 3 with cost of 7'
    assert player1_path[1].to_string() == 'Node b is connected to 3 with cost of 5'
    assert player1_path[2].to_string() == 'Node b is connected to 1 with cost of 3'

    assert player2_path[0].to_string() == 'Node b is connected to 3 with cost of 5'
    assert player2_path[1].to_string() == 'Node 2 is connected to 3 with cost of 6'

    assert player3_path[0].to_string() == 'Node b is connected to 3 with cost of 5'

def test_player_pays_for_edge(graph:Graph):
    pathRule = PathRule(graph=graph)

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))

    player_edges = {'1': player1_edges}

    pathRule.set_player_path_edges(player_edges)

    pathRule.player_pays_for_edges(1)
    assert pathRule.get_cost_allocation() == [11, 0, 0]

def test_update_path_costs(graph:Graph):
    pathRule = PathRule(graph=graph)

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))

    player_edges = {'1': player1_edges,'2':[],'3':[]}

    pathRule.set_player_path_edges(player_edges)

    player_path_costs = {
        '1': 17,
        '2': 3,
        '3': 14
    }
    pathRule.set_player_path_cost(player_path_costs)

    pathRule.update_player_path_costs()
    assert pathRule.get_player_path_cost() == {
        '1': 11,
        '2': 0,
        '3': 0
    }

def test_remove_from_all():
    pathRule = PathRule()

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []
    player3_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    edge_to_remove = Edge(Node(type='source', label='a'), Node(label=1), cost=7)

    pathRule.remove_edge_from_all(edge_to_remove, 3)

    player_path_edges = pathRule.get_player_path_edges()
    player1_path = player_path_edges['1']
    player2_path = player_path_edges['2']
    player3_path = player_path_edges['3']
    assert player1_path[0].to_string() == 'Node 1 is connected to 2 with cost of 4'

    assert player2_path[0].to_string() == 'Node 2 is connected to 3 with cost of 7'
    assert player2_path[1].to_string() == 'Node 1 is connected to 3 with cost of 3'

    assert player3_path[0].to_string() == 'Node a is connected to 1 with cost of 7'

def test_remove_player_edges(graph:Graph):
    pathRule = PathRule(graph=graph)

    player_path_costs = {
        '1': 17,
        '2': 3,
        '3': 14
    }
    pathRule.set_player_path_cost(player_path_costs)

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []
    player3_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player3_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    pathRule.player_remove_edges(3)

    player_path_edges = pathRule.get_player_path_edges()
    player1_path = player_path_edges['1']
    player2_path = player_path_edges['2']
    player3_path = player_path_edges['3']
    assert player1_path[0].to_string() == 'Node 1 is connected to 2 with cost of 4'
    assert len(player1_edges) == 1

    assert player2_path[0].to_string() == 'Node 2 is connected to 3 with cost of 7'
    assert player2_path[1].to_string() == 'Node 1 is connected to 3 with cost of 3'
    assert len(player2_edges) == 2

    assert player3_path == []

    assert pathRule.get_player_path_cost() == {
        '1': 4,
        '2': 10,
        '3': 0
    }

def test_check_for_player_who_can_pay_no(graph:Graph):
    pathRule = PathRule(graph=graph)

    individual_player_costs = {
        '1': 2,
        '2': 1,
        '3': 1
    }
    pathRule.set_individual_cost(individual_player_costs)

    player_path_costs = {
        '1': 20,
        '2': 17,
        '3': 16
    }
    pathRule.set_player_path_cost(player_path_costs)

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []
    player3_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player3_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert pathRule.check_for_player_who_can_pay()

def test_check_for_player_who_can_pay_yes(graph:Graph):
    pathRule = PathRule(graph=graph)

    individual_player_costs = {
        '1': 2,
        '2': 1,
        '3': 20
    }
    pathRule.set_individual_cost(individual_player_costs)

    player_path_costs = {
        '1': 20,
        '2': 17,
        '3': 16
    }
    pathRule.set_player_path_cost(player_path_costs)

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []
    player3_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player3_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert not pathRule.check_for_player_who_can_pay()

    player_path_edges = pathRule.get_player_path_edges()
    player1_path = player_path_edges['1']
    player2_path = player_path_edges['2']
    player3_path = player_path_edges['3']
    assert player1_path[0].to_string() == 'Node 1 is connected to 2 with cost of 4'
    assert len(player1_edges) == 1

    assert player2_path[0].to_string() == 'Node 2 is connected to 3 with cost of 7'
    assert player2_path[1].to_string() == 'Node 1 is connected to 3 with cost of 3'
    assert len(player2_edges) == 2

    assert player3_path == []

    assert pathRule.get_player_path_cost() == {
        '1': 4,
        '2': 10,
        '3': 0
    }

def test_does_one_player_have_edges_all():
    pathRule = PathRule()

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []
    player3_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player3_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert pathRule.does_one_player_have_edges()

def test_does_one_player_have_edges_two():
    pathRule = PathRule()

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []
    player2_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player2_edges.append(Edge(Node(label=2), Node(label=3), cost=7))
    player2_edges.append(Edge(Node(label=1), Node(label=3), cost=3))

    player3_edges = []

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert pathRule.does_one_player_have_edges()

def test_does_one_player_have_edges_one():
    pathRule = PathRule()

    player1_edges = []
    player1_edges.append(Edge(Node(type='source', label='a'), Node(label=1), cost=7))
    player1_edges.append(Edge(Node(label=1), Node(label=2), cost=4))
    player1_edges.append(Edge(Node(type='source', label='b'), Node(label=2), cost=9))

    player2_edges = []

    player3_edges = []

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert pathRule.does_one_player_have_edges()

def test_does_one_player_have_edges_none():
    pathRule = PathRule()

    player1_edges = []

    player2_edges = []

    player3_edges = []

    player_edges = {'1': player1_edges,'2':player2_edges,'3':player3_edges}

    pathRule.set_player_path_edges(player_edges)

    assert not pathRule.does_one_player_have_edges()

def test_get_edge_between_player_and_source(graph:Graph):
    pathRule = PathRule(graph=graph)
    edge = pathRule.getEdgeBetweenPlayerAndSource(1, 'a')

    assert edge.to_string() == 'Node a is connected to 1 with cost of 11'
    
def test_full_run(graph_check:Graph, mcstEdgesCheck:list[Edge]):
    source_a_set = {1}
    source_b_set = {2, 3}
    pathRule = PathRule(graph=graph_check, mcst_edges=mcstEdgesCheck, source_a_set=source_a_set, source_b_set=source_b_set)

    pathRule.run_rule()

    assert pathRule.get_cost_allocation() == [13, 4, 10]

