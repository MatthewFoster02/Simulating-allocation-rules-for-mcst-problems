from cooperative_functions.shapley_value import ShapleyValue

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
