import itertools

class ShapleyValue:
    def __init__(self, coalitions:dict=None, num_players:int=None):
        self.coalitions = coalitions
        self.num_players = num_players

    def get_shapley_value(self):
        # Create all orderings
        # For each ordering, generate a vector with value for each player
        # Average the values given to each player to get Shapley value

        orderings = self.get_all_orderings()

        values = {}
        for order in orderings:
            values[order] = self.get_value(order)
        
        shapley_value = self.average_values(list(values.values()))
        return shapley_value
    
    # TESTED
    def get_all_orderings(self):
        numbers = ''.join(str(i) for i in range(1, self.num_players + 1))
        orderings = [''.join(p) for p in itertools.permutations(numbers)]
        return orderings


    # TESTED
    def get_value(self, order:str):
        value = [0] * self.num_players
        total_allocated_so_far = 0
        for i in range(1, len(order) + 1):
            sub_order = order[:i]
            index_location = int(sub_order[-1]) - 1
            sub_order_ascending = self.sort_order(sub_order)
            this_coalition_value = self.coalitions[sub_order_ascending]
            value[index_location] = this_coalition_value - total_allocated_so_far
            total_allocated_so_far = this_coalition_value
        return value
            
    # TESTED
    def sort_order(self, order:str):
        digits = sorted([int(digit) for digit in order])
        ordered = ''.join(str(digit) for digit in digits)
        return ordered


    #TESTED
    def average_values(self, values:list):
        averages = [sum(items) / len(items) for items in zip(*values)]
        return averages
