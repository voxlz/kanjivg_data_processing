class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
    
    def add_or_append(self, key, value):
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]