# @source: https://hg.python.org/cpython/file/3.6/Lib/heapq.py
class Heap(object):
    """Clase que representa un heap."""

    def __init__(self):
        """Constructor de la clase Heap."""
        self.dicc = {}
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def esta_vacia(self):
        return len(self) == 0

    def __contains__(self, obj):
        return obj in self.dicc

    def __str__(self):
        return str(self.heap)

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, obj, prioridad):
        """Inserta un elemento en el heap."""
        if obj in self.dicc:
            prioridad_ant = self.dicc[obj][0]
            self.dicc[obj][0] = prioridad
            if prioridad > prioridad_ant:
                self._downheap(self.dicc[obj][2])
            elif prioridad < prioridad_ant:
                self._upheap(0, self.dicc[obj][2])
            return

        self.dicc[obj] = [prioridad, obj, len(self)]
        self.heap.append(self.dicc[obj])
        self._upheap(0, len(self)-1)

    def __getitem__(self, obj):
        """Devuelve la prioridad de un elemento en el heap. Si no existe lanza IndexError"""
        return self.dicc[obj][0]

    def popitem(self):
        """Elimina un elemento del heap y devuelve una tupla con el elemento y la prioridad
        respectivamente. Si el heap esta vacio lanza IndexError."""
        self.dicc.pop(self.heap[0][1])
        ultimo = self.heap.pop()    # lanza IndexError si la lista esta vacia
        if self.heap:
            minimo = self.heap[0]
            self.heap[0] = ultimo
            self._downheap(0)
            return (minimo[1], minimo[0])
        return (ultimo[1], ultimo[0])

    def _upheap(self, startpos, pos):
        newitem = self.heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.heap[parentpos]
            if newitem < parent:
                self.heap[pos] = parent
                self.heap[pos][2] = pos
                pos = parentpos
                continue
            break
        self.heap[pos] = newitem
        self.heap[pos][2] = pos

    def _downheap(self, pos):
        endpos = len(self.heap)
        startpos = pos
        newitem = self.heap[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not self.heap[childpos] < self.heap[rightpos]:
                childpos = rightpos
            # Move the smaller child up.
            self.heap[pos] = self.heap[childpos]
            self.heap[pos][2] = pos
            pos = childpos
            childpos = 2*pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        self.heap[pos] = newitem
        self.heap[pos][2] = pos
        self._upheap(startpos, pos)
