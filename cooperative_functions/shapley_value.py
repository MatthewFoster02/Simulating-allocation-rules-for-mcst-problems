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
            values[order] = self.get_values(order)
        
        shapley_value = self.average_values(list(values.values()))
        return shapley_value
    
    # TESTED
    def get_all_orderings(self):
        numbers = ''.join(str(i) for i in range(1, self.num_players + 1))
        orderings = [''.join(p) for p in itertools.permutations(numbers)]
        return orderings

    def get_values(self, order:str):
        pass

    
    #TESTED
    def average_values(self, values:list):
        averages = [sum(items) / len(items) for items in zip(*values)]
        return averages
