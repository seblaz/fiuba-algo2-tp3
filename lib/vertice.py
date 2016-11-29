class Vertice(object):
    """docstring for ."""
    def __init__(self, id, valor):
        self.id     = id
        self.valor  = valor

    def __eq__(a, b):
        return a.id == b.id or a.valor == b.valor

    def __hash__(self):
        return hash((self.id, self.valor))
        # return hash(self.id)
        # return hash(self.valor)+hash(self.id)
