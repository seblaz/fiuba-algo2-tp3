class Vertice(object):
    """Clase que representa un vertice."""
    def __init__(self, nombre, clave, *args):
        """Contructor de la clase Vertice. Parametros:
            -clave: se utilizara para las operaciones de comparacion.
            -args: tuplas de valores extras que se quieran guardar."""
        self.clave = clave
        self.nombre = nombre
        for nombre_dato, arg in args:
            self.__setattr__(nombre_dato,  type(arg))
            self.__dict__[nombre_dato] = arg

    def __lt__(a, b):
        return a.clave < b.clave

    def __str__(self):
        return "({}, {})".format(self.nombre, self.clave)

    def __repr__(self):
        return self.__str__()
