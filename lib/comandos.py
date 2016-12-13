from lib.grafo import Grafo

class Comandos(object):
    """Clase que ejecuta los comandos del grafo."""
    def __init__(self, grafo):
        self.grafo = grafo

    def similares(self, vertice, cantidad):
        return self.grafo.n_similares(vertice, cantidad)

    def recomendar(self, vertice, cantidad):
        return self.grafo.n_recomendar(vertice, cantidad)

    def camino(self, origen, destino):
        return self.grafo.camino(origen, destino)

    def centralidad(self, cantidad):
        return self.grafo.centralidad_exacta(cantidad)
