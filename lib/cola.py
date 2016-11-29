from lib.nodo import Nodo

class Cola:
    """Clase que representa una cola, implementada con nodos."""

    def __init__(self):
        """Constructor de la cola."""
        self._primer_nodo = self._ultimo_nodo = None
        self._cantidad    = 0

    def esta_vacia(self):
        """Devuelve veradadero si la cola esta vacia y falso en caso contrario."""
        return self.__len__() == 0

    def __len__(self):
        """Devuelve la cantidad de elementos en la cola."""
        return self._cantidad

    def encolar(self, dato):
        if self._primer_nodo is None:
            self._primer_nodo = self._ultimo_nodo = Nodo(dato)
        else:
            self._ultimo_nodo.prox = Nodo(dato)
            self._ultimo_nodo = self._ultimo_nodo.prox
        self._cantidad+=1

    def desencolar(self):
        """Desencola un elemento de la cola y lo devuelve. Si la cola esta vacia lanzara IndexError."""
        if self.esta_vacia(): raise IndexError("La cola no tiene elementos")
        nodo = self._primer_nodo
        self._primer_nodo = nodo.prox
        self._cantidad-=1
        return nodo.dato

    def ver_primero(self):
        """Devuelve el primer elemento de la cola. Si la cola esta vacia devuelve None."""
        return None if self.esta_vacia() else self._primer_nodo.dato
