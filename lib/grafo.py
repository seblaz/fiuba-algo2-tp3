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
import operator
import time

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
            - desde y hasta: identificadores de vertices dentro del grafo.
            En caso de no existir la union consultada, se devuelve None.
        '''
        # if not hasta in self._grafo: raise KeyError("No se encuentra el vertice en el grafo.")
        # if not hasta in self._grafo[desde]:
        #     return None
        return self._grafo[desde][hasta]

    def adyacentes(self, valor):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        return self._grafo[valor].keys()

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
                        # print(w, "\t"+padre[w])
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

    def camino_minimo(self, origen, destino, modificar_peso = lambda peso:peso):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - modificar_peso: funcion que recibe un parametro (el peso de una arista) y devuelve un nuevo peso.
            Por defecto, la funcion nula devuelve el mismo peso recibido.
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino.
            En caso que no exista camino entre el origen y el destino, se devuelve None.
        '''
        if not destino in self: raise KeyError("El destino no se encuentra en el grafo.")
        padre = self.sssp(destino, origen, modificar_peso)[0] # pido el camino inverso para luego poder insertar elementos al final de la lista y no al principio. Al ser un grafo no dirigido, es igual.
        actual = origen
        lista = [actual]
        while actual != destino:
            try:
                actual = padre[actual][0]
            except KeyError:
                return None # el grafo no es conexo, porque el origen o alguno de los elementos no tiene padre
            lista.append(actual)
        return lista

    def sssp(self, origen, destino = None, modificar_peso = lambda peso:peso): # (Single-source short path) implementado con Dijkstra
        '''Calcula los caminos minimos desde un vertice origen a todos los vertices alcanzables desde ese vertice a menos que se indice un destino, en cuyo caso terminara la ejecuccion cuando encuentre el camino mas corto al destino.
        Toma como hipotesis que los pesos de los vertices son positivos. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - modificar_peso: funcion que recibe el peso y devuelve un peso modficado.
        Devuelve:
            - un diccionario con los padres de cada vertice. La clave es el hijo y el valor es una tupla con el padre y el peso de la arista, respectivamente. Notar que solo contendra los vertices alcanzables desde el origen.
            - un diccionario con las distancias desde el origen a cada vertice. La clave es vertice y el valor es la distancia.
        '''
        # print(origen)
        # start_time = time.time()

        heap_v      = []
        padre       = {}
        visitados   = {}
        heap_dicc   = {}
        distancia   = {}

        for v in self:
            heap_dicc[v] = float("inf")

        heap_v.append((0, origen))
        padre[origen]       = None
        distancia[origen]   = 0
        heap_dicc[origen]   = 0

        while heap_v:
            prior, ver = heapq.heappop(heap_v)
            visitados[ver] = True # key esta en el camino minimo
            if ver == destino: break
            for v in self.adyacentes(ver):
                if v not in visitados and heap_dicc[v] > heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v)): # relax
                    heapq.heappush(heap_v, (heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v)), v))
                    padre[v] = (ver, self.obtener_peso_arista(ver, v))
                    distancia[v] = distancia[ver] + self.obtener_peso_arista(ver, v)
                    heap_dicc[v] = heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v))

        # padre = {}
        # distancia = {}
        # visitados = {}
        # heap_v = Heap()
        # for v in self:
        #     heap_v[v] = float("inf")
        # heap_v[origen] = 0
        # padre[origen] = None
        # distancia[origen] = 0
        # # print("listo")
        # while heap_v:
        #     key, value = heap_v.popitem()
        #     visitados[key] = True # key esta en el camino minimo
        #     # if key == destino: break
        #     for v in self.adyacentes(key):
        #         if v not in visitados and heap_v[v] > value + modificar_peso(self.obtener_peso_arista(key, v)):# relax
        #             heap_v[v] = value + modificar_peso(self.obtener_peso_arista(key, v))
        #             padre[v] = (key, self.obtener_peso_arista(key, v))
        #             distancia[v] = value + self.obtener_peso_arista(key, v)
        # print("--- %s seconds ---" % (time.time() - start_time))
        return padre, distancia

    @staticmethod
    def crear_grafo_con_padre(padre, es_pesado = False, es_dirigido = False):
        """A partir de un diccionario de padres crea y devuelve un grafo con los respectivos datos. Parametros:
            - padre: un diccionario con los hijos como clave y los padres como valor. Si es pesado los valores son tuplas que se corresponden al padre y al peso de la arista, respectivamente.
            - es_pesado: indica si el grafo sera pesado o no.
            - es_dirigido: indica si el grafo sera dirigido o no.
        Devuelve:
            - un nuevo grafo con los datos correspondientes al diccionario de padres."""
        n_grafo = Grafo(es_dirigido)
        for v in padre.keys():
            n_grafo.add(v)
        if es_pesado:
            for v1, tupla in padre.items():
                if tupla:
                    n_grafo.agregar_arista(v1, tupla[0], tupla[1])
        else:
            for v1, v2 in padre.items():
                if v2:
                    n_grafo.agregar_arista(v1, v2)
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
        dicc_aux = {}
        if not origen:
            origen = random.choice(list(self._grafo.keys()))
        actual = origen
        if not pesado:
            for x in range(largo):
                actual = random.choice(list(self.adyacentes(actual)))
                lista.append(actual)
        else:
            for x in range(largo):
                tot = 0
                for v in self.adyacentes(actual): # esta implementacion es de orden igual a la cantidad de vertices adyacentes.
                    tot+=self.obtener_peso_arista(actual, v)
                rand = random.random()
                for v in self.adyacentes(actual):
                    rand-=self.obtener_peso_arista(actual, v)/tot
                    if rand <= 0:
                        actual = v
                        lista.append(actual)
                        break
                #     for x in range(self.obtener_peso_arista(actual, v)): # esta implementacion es muy practica para aristas de poco peso. Para aristas con un peso 'alto' habria que insertar muchos elementos en lista_aux, lo que lo haria más ineficiente.
                #         lista_aux.append(v)
                # actual = random.choice(lista_aux)
                # lista.append(actual)
                # lista_aux = []
        return lista

    def __str__(self):
        return str(self._grafo)

    def __repr__(self):
        return self.__str__()

    def _similares(self, origen, n, sin_adyacentes = False):
        '''Dado un personaje origen, encuentra los n personajes más similares a este.
        Si sin_adyacentes es True, la lista devuelta no contiene vertices adyacentes al origen. Parámetros:
             -origen: el personaje en cuestión, al que se le buscan los similares.
             -n: la cantidad de personajes semejantes que se desean busca.
             -sin_adyacentes: determina si la lista devuelta contendra o no vertices adyacentes al origen.
        Salida: De mayor a menor similaridad, los n personajes más similares al personaje indicado.'''
        def devolver_frecuencias(lista):
            '''Arma un diccionario con las frecuencias de cada elemento en la lista.
            Parametros:
                -lista: la lista sobre la cual se quiere saber las frecuencias.
            Devuelve:
                -un diccionario con los elementos de la lista como claves y las frecuencias como valor.'''
            dicc_f = {}
            for elem in lista:
                dicc_f[elem] = dicc_f.get(elem, 0)+1
            return dicc_f

        lista = []
        dicc_aux = {}
        if sin_adyacentes:
            for v in self.adyacentes(origen):
                dicc_aux[v] = True
        while len(lista) != n: # realizo random walks de largo n y agrego un personaje a la lista por cada random walk
            dicc_temp = devolver_frecuencias(self.random_walk(n, origen, True))
            lista_temp = sorted(dicc_temp.items(), key=operator.itemgetter(1))
            while lista_temp:
                elem = lista_temp.pop()[0]
                if not elem in dicc_aux:
                    lista.append(elem)
                    dicc_aux[elem] = True
                    break
        return lista

    def n_similares(self, origen, n):
        '''Dado un personaje origen, encuentra los n personajes más similares a este. Parámetros:
             -origen: el personaje en cuestión, al que se le buscan los similares.
             -n: la cantidad de personajes semejantes que se desean busca.
        Salida: De mayor a menor similaridad, los n personajes más similares al personaje indicado.'''
        return self._similares(origen, n, False)

    def n_recomendar(self, origen, n):
        '''Dado un personaje con el cual se quiere realizar un nuevo comic, recomendar otro (u otros) personaje con el cual no haya participado aún en un comic, y sea lo más similar a él posible. Parámetros:
             -origen: el personaje en cuestión, al que se le buscan los similares.
             -n: la cantidad de personajes semejantes que se desean busca.
        Salida: De mayor a menor similaridad, los n personajes más similares al personaje indicado.'''
        return self._similares(origen, n, True)

    def camino(self, origen, destino):
        '''Encuentra el camino mas corto en tiempo entre origen y destino. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
        Devuelve:
            - una lista con el recorrido.'''
        return self.camino_minimo(origen, destino, lambda peso:(1/peso))

    def centralidad_exacta(self, cantidad):
        '''Obtener los personajes más centrales de la red. Los personajes más centrales suelen ser a su vez los más importantes (o lo que se dice en redes sociales, influyente). Parámetros:
            - cantidad: la cantidad de personajes que se desean mostrar.
        Salida: Los ‘cantidad’ Personajes más centrales de la red, mostrado de mayor a menor.
        '''
        cent = {}
        x = 0
        for v in self: cent[v] = 0
        for v in self:

            start_time = time.time()
            padre, distancia = self.dijkstra(v)

            cent_aux = {}

            vertices_ordenados = filter(lambda item: item[1] != float("inf"), distancia.items())
            vertices_ordenados = sorted(vertices_ordenados, key=operator.itemgetter(1), reverse=True)

            for w in distancia.keys(): cent_aux[w] = 0
            for w in vertices_ordenados[:-1]: # no incluyo el origen, porque no tiene padre
                cent_aux[padre[w[0]][0]]+= 1 + cent_aux[w[0]]
            for w in cent_aux:
                if w == v: continue
                cent[w] += cent_aux[w]
            x+=1;
            print("--- %s seconds ---" % (time.time() - start_time))
        print(cent)

    def dijkstra_mejorado(self, origen, caminos): # (Single-source short path) implementado con Dijkstra
        '''Calcula los caminos minimos desde un vertice origen a todos los vertices alcanzables desde ese vertice.
        Toma como hipotesis que los pesos de los vertices son positivos. Parametros:
            - origen: identificador de vertices dentro del grafo. Si no existe dentro del grafo, lanzara KeyError.
            - caminos: un diccionario que guarda los caminos minimos encontrados por dijkstra anteriormente.
        Devuelve:
            - un diccionario con los padres de cada vertice. La clave es el hijo y el valor es una tupla con el padre y el peso de la arista, respectivamente. Notar que solo contendra los vertices alcanzables desde el origen.
            - un diccionario con las distancias desde el origen a cada vertice. La clave es vertice y el valor es la distancia.
        '''
        distancia = {}
        optimizado = {}
        optimizado[origen] = True
        cola = Cola()
        cola.encolar(origen)
        while cola:
            actual = cola.desencolar()
            for v, source in caminos[actual].items():
                if not v in optimizado:
                    distancia[v] = self.obtener_peso_arista(v, actual)
                    optimizado[v] = True
                    if source != v: cola.encolar(v)

        # visitados = {}
        # visitados[origen] = True
        #
        # for v in self.adyacentes(origen):
        #     pass
        #
        # return padre, distancia

        # n_similares anterior
        # lista = []
        # lista_aux = []
        # visitados = {}
        # pesos = {}
        # dic_aux = {}
        # cola = Cola()
        #
        # pesos[origen] = 0
        # visitados[origen] = True
        # cola.encolar(origen)
        #
        # while cola:
        #     while cola:
        #         u = cola.desencolar()
        #         for v in self.adyacentes(u):
        #             if v not in visitados and pesos.get(v, 0) < self.obtener_peso_arista(u, v) + pesos[u]:
        #                 pesos[v] = self.obtener_peso_arista(u, v) + pesos[u]
        #                 dic_aux[v] = pesos[v]
        #
        #     for v, peso in list(dic_aux.items()):
        #         del dic_aux[v]
        #         lista_aux.append(Vertice(v, peso))
        #         visitados[v] = True
        #         cola.encolar(v)
        #
        #     lista_aux.sort()
        #     for x in range(len(lista_aux)):
        #         lista.append(lista_aux.pop().nombre)
        #         if len(lista) == n: return lista
        # return lista

        # camino_minimo anterior
        # return lista if lista[-1] == destino else None # en caso que no sea conexo
        # orden_actual = 0
        #
        # def visitar(v, padre, orden, extra):
        #     if extra[0] != orden[v]:
        #         for x in range(extra[0]-orden[v]):
        #             extra[1].pop()
        #     extra[1].append(v)
        #     extra[0] = orden[v]+1
        #     return v != extra[2]
        #
        # padre, orden = n_grafo.dfs(visitar, [orden_actual, lista, destino], origen)

    def dijkstra(self, origen): # (Single-source short path) implementado con Dijkstra

        heap_v      = []
        padre       = {}
        visitados   = {}
        distancia   = {}

        for v in self:
            distancia[v] = float("inf")

        heap_v.append((0, origen))
        padre[origen]       = None
        distancia[origen]   = 0

        while heap_v:
            prior, ver = heapq.heappop(heap_v)
            visitados[ver] = True # key esta en el camino minimo
            for v in self.adyacentes(ver):
                if v not in visitados and distancia[v] > distancia[ver] + (self.obtener_peso_arista(ver, v)): # relax
                    peso = self.obtener_peso_arista(ver, v)
                    heapq.heappush(heap_v, (distancia[ver] + (peso), v))
                    padre[v] = (ver, peso)
                    distancia[v] = distancia[ver] + peso

        return padre, distancia
        # return padre, distancia2

        heap_v      = []
        padre       = {}
        visitados   = {}
        heap_dicc   = {}
        distancia   = {}

        for v in self:
            heap_dicc[v] = float("inf")

        heap_v.append((0, origen))
        padre[origen]       = None
        distancia[origen]   = 0
        heap_dicc[origen]   = 0

        while heap_v:
            prior, ver = heapq.heappop(heap_v)
            visitados[ver] = True # key esta en el camino minimo
            if ver == destino: break
            for v in self.adyacentes(ver):
                if v not in visitados and heap_dicc[v] > heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v)): # relax
                    heapq.heappush(heap_v, (heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v)), v))
                    padre[v] = (ver, self.obtener_peso_arista(ver, v))
                    distancia[v] = distancia[ver] + self.obtener_peso_arista(ver, v)
                    heap_dicc[v] = heap_dicc[ver] + modificar_peso(self.obtener_peso_arista(ver, v))
