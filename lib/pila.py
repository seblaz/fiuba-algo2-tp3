from lista_enlazada import ListaEnlazada


class _IteradorPila:

    def __init__(self, prim):
        self.actual = prim

    def __next__(self):
        if self.actual is None:
            raise StopIteration()
        dato = self.actual.dato
        self.actual = self.actual.prox
        return dato


class Pila:

    def __init__(self):
        self.items = ListaEnlazada()

    def __str__(self):
        return str(self.items)

    def __iter__(self):
        return _IteradorPila(self.items.prim)

    def esta_vacia(self):
        return self.items.prim is None

    def apilar(self, x):
        self.items.insert(x, 0)

    def desapilar(self):
        if self.esta_vacia():
            raise ValueError('La pila está vacía.')
        return self.items.pop(0)

    def ver_tope(self):
        return self.items.prim.dato
