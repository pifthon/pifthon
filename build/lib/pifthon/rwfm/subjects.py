import rwfm

class Subject:
    def __init__(self, name, label):
        self.name = name
        self.label = label
    
    def __repr__(self):
        return f'{self.name}:{self.label}'