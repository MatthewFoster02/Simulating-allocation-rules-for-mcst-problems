import pytest

from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph
from classical_folk_rule.folk_rule import FolkRule
from first_rule_and_prims.mcst import MCST

@pytest.fixture
def graph_3_players():
    node_source_a = Node(type='source', label='a')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)

    edges = []
    edges.append(Edge(node_source_a, node_player_1, 8))
    edges.append(Edge(node_source_a, node_player_2, 9))
    edges.append(Edge(node_source_a, node_player_3, 8))
    edges.append(Edge(node_player_1, node_player_2, 4))
    edges.append(Edge(node_player_1, node_player_3, 10))
    edges.append(Edge(node_player_2, node_player_3, 5))

    sources = [node_source_a]
    players = [node_player_1, node_player_2, node_player_3]
    return Graph(edges=edges, sources=sources, players=players)

@pytest.fixture
def graph_4_players():
    node_source_a = Node(type='source', label='a')
    node_player_1 = Node(label=1)
    node_player_2 = Node(label=2)
    node_player_3 = Node(label=3)
    node_player_4 = Node(label=4)

    edges = []
    edges.append(Edge(node_source_a, node_player_1, 8))
    edges.append(Edge(node_source_a, node_player_2, 9))
    edges.append(Edge(node_source_a, node_player_3, 8))
    edges.append(Edge(node_source_a, node_player_4, 3))
    edges.append(Edge(node_player_1, node_player_2, 4))
    edges.append(Edge(node_player_1, node_player_3, 10))
    edges.append(Edge(node_player_1, node_player_4, 15))
    edges.append(Edge(node_player_2, node_player_3, 5))
    edges.append(Edge(node_player_2, node_player_4, 16))
    edges.append(Edge(node_player_3, node_player_4, 12))

    sources = [node_source_a]
    players = [node_player_1, node_player_2, node_player_3, node_player_4]
    return Graph(edges=edges, sources=sources, players=players)

def test_share_evenly_one_players(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.share_evenly({1}, 4)
    assert folkRule.get_cost_allocation() == [4, 0, 0]

def test_share_evenly_two_players(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.share_evenly({1, 2}, 4)
    assert folkRule.get_cost_allocation() == [2, 2, 0]

def test_share_evenly_three_players(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.share_evenly({1, 2, 3}, 9)
    assert folkRule.get_cost_allocation() == [3, 3, 3]

def test_share_proportionately_3_players_2_sharing(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.share_proportionately({1}, {2}, 4)
    assert folkRule.get_cost_allocation() == [2, 2, 0]

def test_share_proportionately_3_players_3_sharing(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.share_proportionately({1, 2}, {3}, 12)
    assert folkRule.get_cost_allocation() == [2, 2, 8]

def test_share_proportionately_4_players_3_sharing(graph_4_players:Graph):
    folkRule = FolkRule(source=graph_4_players.get_sources()[0], players=graph_4_players.get_players())
    folkRule.share_proportionately({1, 2}, {4}, 12)
    assert folkRule.get_cost_allocation() == [2, 2, 0, 8]

def test_share_proportionately_4_players_4_sharing(graph_4_players:Graph):
    folkRule = FolkRule(source=graph_4_players.get_sources()[0], players=graph_4_players.get_players())
    folkRule.share_proportionately({1, 2, 3}, {4}, 12)
    assert folkRule.get_cost_allocation() == [1, 1, 1, 9]

def test_share_proportionately_4_players_4_sharing_2_by_2(graph_4_players:Graph):
    folkRule = FolkRule(source=graph_4_players.get_sources()[0], players=graph_4_players.get_players())
    folkRule.share_proportionately({1, 2}, {3, 4}, 12)
    assert folkRule.get_cost_allocation() == [3, 3, 3, 3]

def test_get_component_with_source_first(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    assert folkRule.get_component_with_source({1, 2, 'a'}, {3}) == {1, 2, 'a'}    

def test_get_component_with_source_second(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    assert folkRule.get_component_with_source({1, 2}, {3, 'a'}) == {3, 'a'}    

def test_get_component_with_source_neither(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    assert folkRule.get_component_with_source({1, 2}, {3}) is None

def test_get_component_of_node_player(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.set_components([{1, 2}, {3}, {'a'}])
    assert folkRule.get_component_of_node(1) == {1, 2}

def test_get_component_of_node_source(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    folkRule.set_components([{1, 2}, {3}, {'a'}])
    assert folkRule.get_component_of_node('a') == {'a'}

def test_share_cost_of_edge_3_players_no_source(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    new_edge = Edge(start_node=Node(label=1), end_node=Node(label=3), cost=10)
    components = [{1, 2}, {3}, {'a'}]
    folkRule.share_edge_cost(new_edge, components)
    folk_allocation = folkRule.get_cost_allocation()
    assert 1.6 < folk_allocation[0] < 1.7
    assert 1.6 < folk_allocation[1] < 1.7
    assert 6.6 < folk_allocation[2] < 6.7

def test_share_cost_of_edge_3_players_no_source_2_joining(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    new_edge = Edge(start_node=Node(label=1), end_node=Node(label=3), cost=10)
    components = [{1}, {2}, {3}, {'a'}]
    folkRule.share_edge_cost(new_edge, components)
    assert folkRule.get_cost_allocation() == [5, 0, 5]

def test_share_cost_of_edge_3_players_source_1(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    new_edge = Edge(start_node=Node(label='a'), end_node=Node(label=1), cost=8)
    components = [{1}, {2}, {3}, {'a'}]
    folkRule.share_edge_cost(new_edge, components)
    assert folkRule.get_cost_allocation() == [8, 0, 0]

def test_share_cost_of_edge_3_players_source_3(graph_3_players:Graph):
    folkRule = FolkRule(source=graph_3_players.get_sources()[0], players=graph_3_players.get_players())
    new_edge = Edge(start_node=Node(label='a'), end_node=Node(label=1), cost=8)
    components = [{1, 2, 3}, {'a'}]
    folkRule.share_edge_cost(new_edge, components)
    assert folkRule.get_cost_allocation() == [8/3, 8/3, 8/3]

def test_folk_rule_3_player_graph(graph_3_players:Graph):
    kruskal = MCST(graph=graph_3_players)
    kruskal.kruskal(use_classical_folk_rule=True)
    cost_allocation = kruskal.getCostAllocation()
    assert cost_allocation == [5.5, 5.5, 6]

def test_folk_rule_4_player_graph(graph_4_players:Graph):
    kruskal = MCST(graph=graph_4_players)
    kruskal.kruskal(use_classical_folk_rule=True)
    cost_allocation = kruskal.getCostAllocation()
    assert cost_allocation == [5.5, 5.5, 6, 3]
