V_LINE = "*Vertices "
A_LINE = "*Arcs "

class Pjk(object):
    """Clase para cargar los datos de un archivo Pjk en un grafo."""
    def __init__(self, archivo, grafo):
        '''Constructor de la clase Pjk. Parametros:
            - archivo: nombre del archivo a leer
            - grafo: instancia de la clase grafo donde se cargaran los datos.'''
        self.archivo  = open(archivo, "r")
        self.grafo    = grafo
        self.list_aux = []

    def leer(self):
        '''Lee el archivo y guarda los datos en el vector.'''
        line = self.archivo.readline()
        if V_LINE in line: n_vertices = int(line[len(V_LINE):])
        self.list_aux = [None]*(n_vertices+1)

        for x in range(n_vertices):
            line = self.archivo.readline()
            id, value = line.split(maxsplit = 1)
            self.list_aux[int(id)] = value[1:-2]
            self.grafo.add(value[1:-2])

        line = self.archivo.readline()
        if A_LINE in line: pass
        for line in self.archivo:
            id1, id2, peso = line.split()
            self.grafo.agregar_arista(self.list_aux[int(id1)], self.list_aux[int(id2)], int(peso))

    def cerrar(self):
        '''Cierra el archivo.'''
        self.archivo.close()
