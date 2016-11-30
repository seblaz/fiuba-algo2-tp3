from lib.cola import Cola
from lib.heap import Heap
from lib.vertice import Vertice
from lib.arista import Arista
from lib.heapdict import heapdict
import copy
import queue
import random
import heapq
import sys

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0
INF = "INF"

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''

    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self._grafo       = {}
        self._es_dirigido = es_dirigido

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return len(self._grafo)

    def add(self, valor):
        '''Agrega un nuevo vertice con el valor indicado. Valor debe ser de identificador unico del vertice.'''
        if not valor in self._grafo:
            self._grafo[valor] = {}

    def __delitem__(self, valor):
        '''Elimina el vertice del grafo. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        if not self._es_dirigido: # primero borro las aristas para acceder en O(1)
            for nodo in list(self._grafo[valor].keys()): # list() es necesario para que se cree una copia de las claves
                self.borrar_arista(nodo, valor) # tambien se borra la reciproca
        del self._grafo[valor]
        # En el caso en el que sea un grafo dirigido, tambien se deberian buscar las aristas que entran al nodo.
        # Para ello se deberia realizar una busqueda lineal, o bien guardar en el nodo las aristas que entran al mismo.
        # Dado que para el tp el grafo es no-dirigido, no se implementara dicha parte.
        # Dicha implementacion tampoco es vital, dado que si se intenta obtener el arista a un nodo que ya no existe,
        # lanzara KeyError, aunque grafo.adyacentes() devolveria aristas a nodos inexistentes, pudiendo ocasionar
        # KeyError's inesperados.

    def __contains__(self, valor):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''
        return valor in self._grafo

    def __eq__(a, b):
        return a._grafo == b._grafo

    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        return iter(self._grafo)

    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return self._grafo.keys()

    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        if not hasta in self._grafo: # necesario para grafos no dirigidos
            raise KeyError("Una de las aristas no se encuentra en el grafo")
        self._grafo[desde][hasta] = peso # si desde no existe lanzara KeyError
        if not self._es_dirigido:
            self._grafo[hasta][desde] = peso

    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
           Si el grafo es dirigido, tambien borrara la arista reciproca.
        '''
        if not hasta in self._grafo: raise KeyError("No se encuentra el vertice en el grafo.")
        if not hasta in self._grafo[desde]: # dada la invariante no se necesario chequear el arista reciproca
            raise ValueError("No existe la arista")
        del self._grafo[desde][hasta]
        if not self._es_dirigido:
            del self._grafo[hasta][desde]

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if not hasta in self._grafo: raise KeyError("No se encuentra el vertice en el grafo.")
        if not hasta in self._grafo[desde]:
            return None
        return self._grafo[desde][hasta]

    def adyacentes(self, valor):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        return list(self._grafo[valor].keys())

    def _recorridos(self, visitar, extra, inicio, f_recorrer):
        """Funcion interna que sirve para los recorridos bfs y dfs."""
        visitados = {}
        padre = {}
        orden = {}
        if inicio:
            padre[inicio] = None
            orden[inicio] = 0
            f_recorrer(self, inicio, visitados, padre, orden, visitar, extra)
        else:
            for v in self._grafo:
                if v not in visitados:
                    padre[v] = None
                    orden[v] = 0
                    if not f_recorrer(self, v, visitados, padre, orden, visitar, extra): break
        return padre, orden

    def bfs(self, visitar = visitar_nulo, extra = None, inicio = None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo:
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual,
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar).
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice,
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        def bfs_visitar(grafo, origen, visitados, padre, orden, visitar, extra):
            q = Cola()
            q.encolar(origen)
            visitados[origen] = True
            if not visitar(origen, padre, orden, extra): return False
            while len(q) > 0:
                v = q.desencolar()
                for w in grafo.adyacentes(v):
                    if w not in visitados:
                        visitados[w] = True
                        padre[w] = v
                        orden[w] = orden[v] + 1
                        if not visitar(w, padre, orden, extra): return False
                        q.encolar(w)
            return True

        return self._recorridos(visitar, extra, inicio, bfs_visitar)


    def dfs(self, visitar = visitar_nulo, extra = None, inicio = None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo:
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual,
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar).
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice,
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        def dfs_visitar(grafo, v, visitados, padre, orden, visitar, extra):
            visitados[v] = True
            if not padre[v] and not visitar(v, padre, orden, extra): return False
            for w in grafo.adyacentes(v):
                if w not in visitados:
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    if not visitar(w, padre, orden, extra): return False
                    if not dfs_visitar(grafo, w, visitados, padre, orden, visitar, extra): return False
            # para implementar el orden topologico, aca abria que insertar el elemento en la lista enlazada (solo paragrafos dirigidos)
            return True

        return self._recorridos(visitar, extra, inicio, dfs_visitar)

    def transpuesto(self):
        '''Devuelve un nuevo grafo con sus aristas transpuestas.
        Solamente tiene sentido de aplicar en grafos dirigidos, por lo que
        en caso de aplicarse a un grafo no-dirigido se lanzara TypeError'''
        if not self._es_dirigido: raise TypeError("Los grafos transpuestos aplican solamente a grafos no dirigidos")
        nuevo = copy.deepcopy(self)
        for vertice in self:
            for arista in self._grafo[vertice]:
                nuevo.agregar_arista(arista, vertice)
                nuevo.borrar_arista(vertice, arista)
        return nuevo

    def scc(self): # SCC (Strongly Conected Components)
        '''Devuelve dos diccionarios.
        El primer diccionario contiene los vertices que componen cada componente fuertemente conexa como clave y un numero identificatorio de la componente conexa como valor.
        El segundo contiene el numero identificatorio de la componente fuertemente conexa como clave y un diccionario que representa las aristas entre componentes fuertemente conexas como valor. El diccionario de aristas posee el identificador de la componente conexa a la que esta conectada como clave y el peso como valor.
        Solamente tiene sentido de aplicar en grafos dirigidos, por lo que en caso de aplicarse a un grafo no-dirigido se lanzara TypeError'''
        if not self._es_dirigido: raise TypeError("Las componentes fuertemente conexas aplican solamente a grafos dirigidos")
        raise NotImplementedError() # No es necesario para el tp

    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
        if self._es_dirigido: raise TypeError("Las componentes conexas aplican solamente a grafos no dirigidos")
        def visitar(v, padre, orden, lista):
            if not padre[v]: # nueva componente conexa
                lista.append([v])
            else: # inserto el nodo en la ultima lista de la lista
                lista[-1].append(v)
            return True
        lista = []
        self.bfs(visitar, lista, None)
        return lista

    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino.
            En caso que no exista camino entre el origen y el destino, se devuelve None.
        '''
        if not destino in self: raise KeyError("El destino no se encuentra en el grafo.")
        n_grafo = self.sssp(origen, destino)
        lista = []
        orden_actual = 0

        def visitar(v, padre, orden, extra):
            if extra[0] != orden[v]:
                for x in range(extra[0]-orden[v]):
                    extra[1].pop()
            extra[1].append(v)
            extra[0] = orden[v]+1
            return v != extra[2]

        padre, orden = n_grafo.dfs(visitar, [orden_actual, lista, destino], origen)
        return lista if lista[-1] == destino else None # en caso que no sea conexo

    def sssp(self, origen, destino = None): # (Single-source short path)
        '''Calcula los caminos minimos desde un vertice origen a todos los vertices alcanzables desde ese vertice a menos que se indice un destino, en cuyo caso terminara la ejecuccion cuando encuentre el camino mas corto al destino.
        Toma como hipotesis que los pesos de los vertices son positivos. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
        Devuelve:
            - un nuevo grafo, con los mismos vertices que el original, pero en con los caminos minimos desde el origen.
        '''
        n_grafo = Grafo(self._es_dirigido)
        padre = {}
        visitados = {}
        heap_v = heapdict()
        for v in self:
            n_grafo.add(v)
            heap_v[v] = float("inf")
        heap_v[origen] = 0
        visitados[origen] = True
        padre[origen] = None

        while heap_v:
            key, value = heap_v.popitem()
            visitados[key] = True # key esta en el camino minimo
            if destino and key == destino: break
            for v in self.adyacentes(key):
                if v not in visitados and heap_v[v] > value + self.obtener_peso_arista(key, v):# relax
                    for a in list(n_grafo._grafo[v]):
                        n_grafo.borrar_arista(a, v)
                    n_grafo.agregar_arista(key, v, self.obtener_peso_arista(key, v))
                    heap_v[v] = value + self.obtener_peso_arista(key, v)
                    padre[v] = key
        return n_grafo

    def mst(self): # Calculado con Kruskal
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion de tipo TypeError.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        if self._es_dirigido: raise TypeError("El Arbol de Tendido Minimo se calcula para grafos no dirigidos.")

        n_grafo = Grafo()
        set_princ = {} # representacion de un disjoint-set.
        set_aux   = {} # estructura aux para representar el set
        l_aristas = []

        for v in self:
            n_grafo.add(v)
            set_princ[v] = v
            set_aux[v]   = [v]
            for a in self._grafo[v]:
                l_aristas.append(Arista(v, a, self.obtener_peso_arista(v, a)))
        l_aristas.sort()

        for a in l_aristas:
            if set_princ[a.v1] != set_princ[a.v2]:
                n_grafo.agregar_arista(a.v1, a.v2, self.obtener_peso_arista(a.v1, a.v2))
                for v in set_aux[a.v2]:
                    set_princ[v] = set_princ[a.v1]
                    set_aux[a.v1].append(v)
                    set_aux[v] = set_aux[a.v1]
        return n_grafo

    def random_walk(self, largo, origen = None, pesado = False):
        ''' Devuelve una lista con un recorrido aleatorio de grafo.
            Parametros:
                - largo: El largo del recorrido a realizar
                - origen: Vertice (id) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
                - pesado: indica si se tienen en cuenta los pesos de las aristas para determinar las probabilidades de movernos de un vertice a uno de sus vecinos (False = todo equiprobable).
            Devuelve:
                Una lista con los vertices (ids) recorridos, en el orden del recorrido.
        '''
        lista = []
        lista_aux = []
        if not origen:
            origen = random.choice(list(self._grafo.keys()))
        actual = origen
        if not pesado:
            for x in range(largo):
                actual = random.choice(self.adyacentes(actual))
                lista.append(actual)
        else:
            for x in range(largo):
                for v in self.adyacentes(actual):
                    for x in range(self.obtener_peso_arista(actual, v)):
                        lista_aux.append(v)
                actual = random.choice(lista_aux)
                lista.append(actual)
                lista_aux = []
        return lista

    def __str__(self):
        return str(self._grafo)

    def __repr__(self):
        return self.__str__()
