import rwfm

class Object:
    def __init__(self, name, value, label):
        self.name = name
        self.value = value
        self.label = label

    def __repr__(self):
        return f'{self.name}:{self.value}:{self.label}'
