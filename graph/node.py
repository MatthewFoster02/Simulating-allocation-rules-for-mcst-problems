class Node:
    def __init__(self, type:str='player', label:str=''):
        self.type = type
        self.label = label
    
    def set_type(self, type:str):
        self.type = type
    
    def get_type(self):
        return self.type
    
    def set_label(self, label:str):
        self.label = label
    
    def get_label(self):
        return self.label
