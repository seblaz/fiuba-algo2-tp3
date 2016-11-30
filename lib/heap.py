import heapq

class Heap(object):
    """Clase que representa un heap de minimos."""

    def __init__(self):
        self._vec = []
        self._cantidad = 0

    def __len__(self):
        return self._cantidad

    def esta_vacia(self):
        return len(self) == 0

    def __setitem__(self, priority, value):
        heapq.heappush(self._vec, _Nodo_Heap(priority, value))
        self._cantidad+=1

    def pop(self):
        elem = heapq.heappop(self._vec)
        self._cantidad-=1
        return elem._value

    def __contains__(self, value):
        for elem in self._vec:
            if elem._value == value:
                return True
        return False

class _Nodo_Heap(object):
    """Clase que representa un nodo de heap."""
    def __init__(self, priority, value):
        self._priority = priority
        self._value = value

    def __lt__(a, b):
        return a._priority < b._priority
