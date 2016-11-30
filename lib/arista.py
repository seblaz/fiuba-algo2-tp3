class Arista(object):
    """Clase que representa una arista."""
    def __init__(self, v1, v2, peso=1):
        """Contructor de la clase Arista. Parametros:
            -v1: vertice 1.
            -v2: vertice 2.
            -peso: peso de la arista."""
        self.v1 = v1
        self.v2 = v2
        self.peso = peso

    def __eq__(a, b):
        return (a.v1 == b.v1 or a.v1 == b.v2) and (a.v2 == b.v1 or a.v2 == b.v2)

    def __lt__(a, b):
        return a.peso < b.peso

    def __str__(self):
        return "({}, {}, {})".format(self.v1, self.v2, self.peso)

    def __repr__(self):
        return self.__str__()
