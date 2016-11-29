class Nodo:
    """Clase que modela nodos de una lista enlazada."""

    def __init__(self, dato=None, prox=None):
        """Contructor del nodo. El parametro 'dato' indica el dato que almacenara el nodo y 'prox'
        el siguiente nodo."""
        self.dato = dato
        self.prox = prox

    def __str__(self):
        """Devuelve una representacion de tipo string del dato del nodo."""
        return str(self.dato)

    def __repr__(self):
        """Devuelve una representacion de tipo string del dato del nodo."""
        self.__str__()
