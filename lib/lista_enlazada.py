from nodo import _Nodo


class _IteradorListaEnlazada:
    """Modela el iterador de una lista enlazada."""

    def __init__(self, prim):
        """Constructor del iterador de la lista enlazada."""
        self.actual = prim

    def __next__(self):
        """Método para avanzar en el iterador."""
        if self.actual is None:
            raise StopIteration()
        dato = self.actual.dato
        self.actual = self.actual.prox
        return dato


class ListaEnlazada:
    """Modela una lista enlazada."""

    def __init__(self):
        """Crea una lista enlazada vacía."""
        # referencia al primer nodo (None si la lista está vacía)
        self.prim = None
        # cantidad de elementos de la lista
        self.len = 0

    def __len__(self):
        return self.len

    def __str__(self):
        result = '['
        node = self.prim
        if node is not None:
            result += str(node.dato)
            node = node.prox
            while node is not None:
                result += ', ' + str(node.dato)
                node = node.prox
        result += ']'
        return result

    def __iter__(self):
        return _IteradorListaEnlazada(self.prim)

    def pop(self, i=None):
        """Elimina el nodo de la posición i, y devuelve el dato contenido.
        Si i está fuera de rango, se levanta la excepción IndexError.
        Si no se recibe la posición, elimina el último elemento.
        """
        if i is None:
            i = self.len - 1
        if i < 0 or i >= self.len:
            raise IndexError("Índice fuera de rango")
        if i == 0:
            # Caso particular: saltear la cabecera de la lista
            dato = self.prim.dato
            self.prim = self.prim.prox
        else:
            # Buscar los nodos en las posiciones (i-1) e (i)
            n_ant = self.prim
            n_act = n_ant.prox
            for pos in range(1, i):
                n_ant = n_act
                n_act = n_ant.prox
            # Guardar el dato y descartar el nodo
            dato = n_act.dato
            n_ant.prox = n_act.prox
        self.len -= 1
        return dato

    def insert(self, x, i=None):
        """Inserta el elemento x en la posición i.
        Si no se especifica una posicion, se inserta al final.
        Si la posición es inválida, levanta IndexError.
        """
        if i is None:
            i = self.len
        if i < 0 or i > self.len:
            raise IndexError("Posición inválida")
        nuevo = _Nodo(x)
        if i == 0:
            # Caso particular: insertar al principio
            nuevo.prox = self.prim
            self.prim = nuevo
        else:
            # Buscar el nodo anterior a la posición deseada
            n_ant = self.prim
            for pos in range(1, i):
                n_ant = n_ant.prox
            # Intercalar el nuevo nodo
            nuevo.prox = n_ant.prox
            n_ant.prox = nuevo
        self.len += 1

    def get_elemento(self, i):
        """Deuelve el elemento de la posición i.
        Si la posición es inválida, levanta IndexError.
        """
        if i < 0 or i > self.len - 1:
            raise IndexError("Posición inválida")
        if i == 0:
            return self.prim.dato
        nodo = self.prim
        for pos in range(0, i):
            nodo = nodo.prox
        return nodo.dato

    def esta_vacia(self):
        """Devuelve True si la lista esta vacia y False si contiene algun elemento"""
        return self.len == 0

    def index(self, x):
        """Recibe un elemento x y devuelve un entero con la primera posición que encuentra de dicho elemento."""
        i = 0
        for nodo in self:
            if nodo == x:
                return i
            i += 1
