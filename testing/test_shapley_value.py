import pytest

from cooperative_functions.shapley_value import ShapleyValue

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
