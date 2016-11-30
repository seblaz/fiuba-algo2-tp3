from lib.grafo import Grafo
from lib.pruebas.testing import *

def run(pruebas_volumen = 100):
    print("~ Pruebas Grafo ~")
    pruebas_grafo_vacio()
    pruebas_grafo_un_elemento()
    pruebas_grafo_varios_elementos()
    pruebas_grafo_bfs()
    pruebas_grafo_transpuesto()
    pruebas_grafo_componentes_conexas()
    pruebas_grafo_mst()
    pruebas_grafo_sssp()
    pruebas_grafo_camino_minimo()
    pruebas_grafo_random_walk()

def pruebas_grafo_vacio():
    grafo = Grafo()
    print_test("Pruebas Grafo, el grafo no es None", grafo is not None)
    print_test("Pruebas Grafo, la cantidad de elementos es cero", len(grafo) == 0)
    print_test("Pruebas Grafo, el grafo no contiene elementos", "test" not in grafo)
    print_test("Pruebas Grafo, la lista de claves del grafo esta vacia", not grafo.keys())
    print_exception(grafo.__delitem__, KeyError, "Pruebas Grafo, eliminar un elemento lanza KeyError", "test") # se utiliza __delitem__ directamente para utilizar la funcion 'print_exception', pero es equivalente a 'del grafo["test"]'
    print_exception(grafo.borrar_arista, KeyError, "Pruebas Grafo, borrar arista lanza KeyError", "test", "test2")
    print_exception(grafo.obtener_peso_arista, KeyError, "Pruebas Grafo, obtener peso arista lanza KeyError", "test", "test2")
    print_exception(grafo.adyacentes, KeyError, "Pruebas Grafo, obtener adyacentes lanza KeyError", "test")

def pruebas_grafo_un_elemento():
    grafo = Grafo()
    var = "iron"
    grafo.add(var)
    print_test("Pruebas Grafo, el grafo no es None", grafo is not None)
    print_test("Pruebas Grafo, la cantidad de elementos es uno", len(grafo) == 1)
    print_test("Pruebas Grafo, el grafo contiene a 'var'", var in grafo)
    print_test("Pruebas Grafo, la lista de claves del grafo tiene largo uno", len(grafo.keys()) == 1)
    print_test("Pruebas Grafo, la lista de claves del grafo tiene el elemento 'var'", var in grafo.keys())
    print_test("Pruebas Grafo, la lista de adyacentes de 'var' esta vacia", not grafo.adyacentes(var))

    print_exception(grafo.borrar_arista, KeyError, "Pruebas Grafo, borrar arista lanza KeyError", var, "maiden")
    print_exception(grafo.obtener_peso_arista, KeyError, "Pruebas Grafo, obtener peso arista lanza KeyError", var, "maiden")
    print_exception(grafo.adyacentes, KeyError, "Pruebas Grafo, obtener adyacentes lanza KeyError", "test")

    del grafo[var]
    print_test("Pruebas Grafo, despues de elminar 'var' la cantidad de elementos es cero", len(grafo) == 0)
    print_test("Pruebas Grafo, despues de elminar 'var' el grafo no contiene a 'var'", var not in grafo)
    print_test("Pruebas Grafo, despues de elminar 'var' la lista de claves del grafo esta vacia", not grafo.keys())
    print_exception(grafo.__delitem__, KeyError, "Pruebas Grafo, despues de elminar 'var' eliminar un elemento lanza KeyError", var) # se utiliza __delitem__ directamente para utilizar la funcion 'print_exception', pero es equivalente a 'del grafo["test"]'
    print_exception(grafo.adyacentes, KeyError, "Pruebas Grafo, despues de elminar 'var' obtener adyacentes lanza KeyError", var)

def pruebas_grafo_varios_elementos():
    grafo = Grafo()
    vars = ["iron", "maiden", "black", "sabbath"]
    for value in vars:
        grafo.add(value)

    print_test("Pruebas Grafo, la cantidad de elementos es cuatro", len(grafo) == 4)
    for value in vars:
        ok = value in grafo
        if not ok: break
        ok2 = value in grafo.keys()
        if not ok2: break

    print_test("Pruebas Grafo, todos los elementos estan contenidos en el grafo", ok)
    print_test("Pruebas Grafo, todos los elementos estan contenidos en el grafo las claves del grafo", ok2)

    grafo.agregar_arista(vars[0], vars[1])      #
    grafo.agregar_arista(vars[0], vars[2])      # |0|------|1|
    grafo.agregar_arista(vars[1], vars[2])      #  |  -.    |
    grafo.agregar_arista(vars[1], vars[3])      #  |     -. |
    grafo.agregar_arista(vars[2], vars[3])      # |2|------|3|

    print_test("Pruebas Grafo, la arista existe", grafo.obtener_peso_arista(vars[0], vars[1]))
    print_test("Pruebas Grafo, la arista opuesta existe", grafo.obtener_peso_arista(vars[1], vars[0]))
    print_test("Pruebas Grafo, la arista existe", grafo.obtener_peso_arista(vars[0], vars[2]))
    print_test("Pruebas Grafo, la arista opuesta existe", grafo.obtener_peso_arista(vars[2], vars[1]))
    print_test("Pruebas Grafo, la arista existe", grafo.obtener_peso_arista(vars[1], vars[2]))
    print_test("Pruebas Grafo, la arista opuesta existe", grafo.obtener_peso_arista(vars[2], vars[1]))
    print_test("Pruebas Grafo, la arista existe", grafo.obtener_peso_arista(vars[1], vars[3]))
    print_test("Pruebas Grafo, la arista opuesta existe", grafo.obtener_peso_arista(vars[3], vars[1]))
    print_test("Pruebas Grafo, la arista existe", grafo.obtener_peso_arista(vars[2], vars[3]))
    print_test("Pruebas Grafo, la arista opuesta existe", grafo.obtener_peso_arista(vars[3], vars[2]))

    print_test("Pruebas Grafo, adyacentes ok", all(x in [vars[1], vars[2]] for x in grafo.adyacentes(vars[0])))
    print_test("Pruebas Grafo, adyacentes ok", all(x in [vars[0], vars[2], vars[3]] for x in grafo.adyacentes(vars[1])))
    print_test("Pruebas Grafo, adyacentes ok", all(x in [vars[0], vars[1], vars[3]] for x in grafo.adyacentes(vars[2])))
    print_test("Pruebas Grafo, adyacentes ok", all(x in [vars[1], vars[2]] for x in grafo.adyacentes(vars[3])))

    for vertice1 in grafo: # borro todas las aristas
        for vertice2 in grafo:
            try:
                grafo.borrar_arista(vertice1, vertice2)
            except ValueError:
                pass

    for vertice1 in grafo: # chequeo que no halla aristas
        for vertice2 in grafo:
            ok = grafo.obtener_peso_arista(vertice1, vertice2)
            if ok: break
        if ok: break

    print_test("Pruebas Grafo, borrar aristas ok", not ok)
    print_test("Pruebas Grafo, la cantidad de elementos es cuatro", len(grafo) == 4)

    grafo.agregar_arista(vars[0], vars[1])      #
    grafo.agregar_arista(vars[0], vars[2])      # |0|------|1|
    grafo.agregar_arista(vars[1], vars[2])      #  |  -.    |
    grafo.agregar_arista(vars[1], vars[3])      #  |     -. |
    grafo.agregar_arista(vars[2], vars[3])      # |2|------|3|

    del grafo[vars[0]]
    print_test("Pruebas Grafo, el nodo borrado no pertenece al grafo", not vars[0] in grafo)
    print_exception(grafo.obtener_peso_arista, KeyError, "Pruebas Grafo, obtener peso arista borrada lanza KeyError", vars[0], vars[1])
    print_exception(grafo.obtener_peso_arista, KeyError, "Pruebas Grafo, obtener peso arista reciproca borrada lanza KeyError", vars[1], vars[0])
    print_test("Pruebas Grafo, la cantidad de elementos es tres", len(grafo) == 3)
    print_test("Pruebas Grafo, la cantidad de elementos de grafo.keys() es tres", len(grafo.keys()) == 3)

    print_test("Pruebas Grafo, adyacentes ok", vars[0] not in grafo.adyacentes(vars[1]))
    print_test("Pruebas Grafo, adyacentes ok", vars[0] not in grafo.adyacentes(vars[2]))
    print_test("Pruebas Grafo, adyacentes ok", vars[0] not in grafo.adyacentes(vars[3]))

def pruebas_grafo_bfs():
    grafo = Grafo()
    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")

    grafo.agregar_arista("A", "B")
    grafo.agregar_arista("A", "C")
    grafo.agregar_arista("B", "C")
    grafo.agregar_arista("C", "D")
    grafo.agregar_arista("C", "E")
    grafo.agregar_arista("F", "G")
    grafo.agregar_arista("G", "C")

    padre, orden = grafo.bfs(inicio="A")
    # en bfs el arbol de orden debe ser igual para cualquier caso
    print_test("Pruebas Grafo, bfs ok", orden["A"] == 0)
    print_test("Pruebas Grafo, bfs ok", orden["B"] == 1)
    print_test("Pruebas Grafo, bfs ok", orden["C"] == 1)
    print_test("Pruebas Grafo, bfs ok", orden["D"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["E"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["G"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["F"] == 3)

def pruebas_grafo_transpuesto():
    grafo = Grafo()
    print_exception(grafo.transpuesto, TypeError, "Pruebas Grafo, grafo transpuesto en un grafo no-dirigido lanza TypeError")

    grafo = Grafo(True)
    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")

    grafo.agregar_arista("A", "B")
    grafo.agregar_arista("A", "C")
    grafo.agregar_arista("B", "C")
    grafo.agregar_arista("C", "D")
    grafo.agregar_arista("C", "E")
    grafo.agregar_arista("F", "G")
    grafo.agregar_arista("G", "C")

    grafo_t = grafo.transpuesto()
    print_test("Pruebas Grafo, elementos del grafo transpuesto ok", len(grafo_t) == 7)
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", not grafo_t.adyacentes("A"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "A" in grafo_t.adyacentes("B"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "A" in grafo_t.adyacentes("C"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "B" in grafo_t.adyacentes("C"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "G" in grafo_t.adyacentes("C"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "C" in grafo_t.adyacentes("D"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "C" in grafo_t.adyacentes("E"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", not grafo_t.adyacentes("F"))
    print_test("Pruebas Grafo, adyacentes del grafo transpuesto ok", "F" in grafo_t.adyacentes("G"))

    print_test("Pruebas Grafo, elementos del grafo original ok", len(grafo) == 7)
    print_test("Pruebas Grafo, grafo original ok", "B" in grafo.adyacentes("A"))
    print_test("Pruebas Grafo, grafo original ok", "C" in grafo.adyacentes("A"))
    print_test("Pruebas Grafo, grafo original ok", "C" in grafo.adyacentes("B"))
    print_test("Pruebas Grafo, grafo original ok", "D" in grafo.adyacentes("C"))
    print_test("Pruebas Grafo, grafo original ok", "E" in grafo.adyacentes("C"))
    print_test("Pruebas Grafo, grafo original ok", "C" in grafo.adyacentes("G"))
    print_test("Pruebas Grafo, grafo original ok", "G" in grafo.adyacentes("F"))

def pruebas_grafo_componentes_conexas():
    grafo = Grafo(True)
    print_exception(grafo.componentes_conexas, TypeError, "Pruebas Grafo, componentes conexas de un grafo dirigido lanza TypeError")

    grafo = Grafo()
    print_test("Pruebas Grafo, componentes conexas de un grafo vacio es None", not grafo.componentes_conexas())

    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")

    grafo.agregar_arista("A", "B")
    grafo.agregar_arista("A", "C")
    grafo.agregar_arista("B", "C")
    grafo.agregar_arista("C", "D")
    grafo.agregar_arista("C", "E")
    grafo.agregar_arista("F", "G")
    # grafo.agregar_arista("G", "C")

    comp_conx = grafo.componentes_conexas()
    print_test("Pruebas Grafo, cantidad componentes conexas es dos", len(comp_conx)==2)
    if "F" in comp_conx[0]:
        print_test("Pruebas Grafo, primera componente conexa ok", comp_conx[0] == ["G","F"] or comp_conx[0] == ["F","G"])
        print_test("Pruebas Grafo, segunda componente conexa ok", "A" in comp_conx[1])
        print_test("Pruebas Grafo, segunda componente conexa ok", "B" in comp_conx[1])
        print_test("Pruebas Grafo, segunda componente conexa ok", "C" in comp_conx[1])
        print_test("Pruebas Grafo, segunda componente conexa ok", "D" in comp_conx[1])
        print_test("Pruebas Grafo, segunda componente conexa ok", "E" in comp_conx[1])
    else:
        print_test("Pruebas Grafo, primera componente conexa ok", comp_conx[1] == ["G","F"] or comp_conx[1] == ["F","G"])
        print_test("Pruebas Grafo, segunda componente conexa ok", "A" in comp_conx[0])
        print_test("Pruebas Grafo, segunda componente conexa ok", "B" in comp_conx[0])
        print_test("Pruebas Grafo, segunda componente conexa ok", "C" in comp_conx[0])
        print_test("Pruebas Grafo, segunda componente conexa ok", "D" in comp_conx[0])
        print_test("Pruebas Grafo, segunda componente conexa ok", "E" in comp_conx[0])

def visitar_y_sumar(v, padre, orden, suma):
    if padre[v]:
        suma[0]+=suma[1].obtener_peso_arista(v, padre[v])
    return True

def pruebas_grafo_mst(): # Ejemplo del capitulo 23 de Cormen
    grafo = Grafo(True)
    print_exception(grafo.componentes_conexas, TypeError, "Pruebas Grafo, mst de un grafo dirigido lanza TypeError")

    grafo = Grafo()
    print_test("Pruebas Grafo, MST de un grafo vacio es None", not grafo.mst())

    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")
    grafo.add("H")
    grafo.add("I")

    grafo.agregar_arista("A", "B", 4)
    grafo.agregar_arista("A", "H", 8)
    grafo.agregar_arista("B", "C", 8)
    grafo.agregar_arista("B", "H", 8)
    grafo.agregar_arista("C", "D", 7)
    grafo.agregar_arista("C", "F", 4)
    grafo.agregar_arista("C", "I", 2)
    grafo.agregar_arista("D", "E", 9)
    grafo.agregar_arista("D", "F", 14)
    grafo.agregar_arista("E", "F", 10)
    grafo.agregar_arista("F", "G", 2)
    grafo.agregar_arista("G", "I", 6)
    grafo.agregar_arista("G", "H", 1)
    grafo.agregar_arista("H", "I", 7)

    n_grafo = grafo.mst()
    suma = [0, n_grafo]

    n_grafo.dfs(visitar_y_sumar, suma)
    print_test("Pruebas Grafo, la suma del mst conexo es correcta", suma[0] == 37)

    grafo.borrar_arista("B", "H")
    grafo.borrar_arista("B", "C")
    grafo.borrar_arista("H", "G")
    grafo.borrar_arista("H", "I") # el grafo ya no es conexo
    n_grafo = grafo.mst() # se deberian formar dos arboles

    suma = [0, n_grafo]
    n_grafo.dfs(visitar_y_sumar, suma, "A") # primer arbol
    print_test("Pruebas Grafo, la suma del primer arbol del mst no conexo es correcta", suma[0] == 12)

    suma = [0, n_grafo]
    n_grafo.dfs(visitar_y_sumar, suma, "I") # segundo arbol
    print_test("Pruebas Grafo, la suma del segundo arbol del mst no conexo es correcta", suma[0] == 24)

def pruebas_grafo_sssp():
    grafo = Grafo()
    print_exception(grafo.sssp, KeyError, "Pruebas Grafo, sssp  con una clave que no existe en lanza KeyError", "A")

    grafo.add("A")
    print_test("Pruebas Grafo, sssp en un grafo unitario es el mismo grafo", grafo.sssp("A") == grafo)

    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")
    grafo.add("H")
    grafo.add("I")

    grafo.agregar_arista("A", "B", 4)
    grafo.agregar_arista("A", "H", 8)
    grafo.agregar_arista("B", "C", 8)
    grafo.agregar_arista("B", "H", 8)
    grafo.agregar_arista("C", "D", 7)
    grafo.agregar_arista("C", "F", 4)
    grafo.agregar_arista("C", "I", 2)
    grafo.agregar_arista("D", "E", 9)
    grafo.agregar_arista("D", "F", 14)
    grafo.agregar_arista("E", "F", 10)
    grafo.agregar_arista("F", "G", 2)
    grafo.agregar_arista("G", "I", 6)
    grafo.agregar_arista("G", "H", 1)
    grafo.agregar_arista("H", "I", 7)

    n_grafo = grafo.sssp("A")
    suma = [0, n_grafo]
    n_grafo.dfs(visitar_y_sumar, suma, "A")
    print_test("Pruebas Grafo, la suma de las distancias minimas desde 'A' a todos los vertices es correcta", suma[0] == 42)

    grafo.borrar_arista("B", "H")
    grafo.borrar_arista("B", "C")
    grafo.borrar_arista("H", "G")
    grafo.borrar_arista("H", "I") # el grafo ya no es conexo
    n_grafo = grafo.sssp("A")

    suma = [0, n_grafo]
    n_grafo.dfs(visitar_y_sumar, suma, "A")
    print_test("Pruebas Grafo, la suma de las distancias minimas desde 'A' a todos los vertices es correcta", suma[0] == 12)

    comp_conx = n_grafo.componentes_conexas()
    print_test("Pruebas Grafo, las componentes conexas del grafo de distancias minimas desde 'A' es 7", len(comp_conx) == 7)

def pruebas_grafo_camino_minimo():
    grafo = Grafo()
    print_exception(grafo.sssp, KeyError, "Pruebas Grafo, camino minimo con una clave que no existe en lanza KeyError", "A")

    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")
    grafo.add("H")
    grafo.add("I")

    grafo.agregar_arista("A", "B", 4)
    grafo.agregar_arista("A", "H", 8)
    grafo.agregar_arista("B", "C", 8)
    grafo.agregar_arista("B", "H", 8)
    grafo.agregar_arista("C", "D", 7)
    grafo.agregar_arista("C", "F", 4)
    grafo.agregar_arista("C", "I", 2)
    grafo.agregar_arista("D", "E", 9)
    grafo.agregar_arista("D", "F", 14)
    grafo.agregar_arista("E", "F", 10)
    grafo.agregar_arista("F", "G", 2)
    grafo.agregar_arista("G", "I", 6)
    grafo.agregar_arista("G", "H", 1)
    grafo.agregar_arista("H", "I", 7)

    print_test("Pruebas Grafo, camino minimo A-A es correcto", grafo.camino_minimo("A", "A") == ["A"])
    print_test("Pruebas Grafo, camino minimo A-I es correcto", grafo.camino_minimo("A", "I") == ["A", "B", "C", "I"])
    print_test("Pruebas Grafo, camino minimo A-E es correcto", grafo.camino_minimo("A", "E") == ["A", "H", "G", "F", "E"])
    print_test("Pruebas Grafo, camino minimo I-A es correcto", grafo.camino_minimo("I", "A") == ["I", "C", "B", "A"])
    print_test("Pruebas Grafo, camino minimo C-F es correcto", grafo.camino_minimo("C", "F") == ["C", "F"])

    grafo.borrar_arista("B", "H")
    grafo.borrar_arista("B", "C")
    grafo.borrar_arista("H", "G")
    grafo.borrar_arista("H", "I") # el grafo ya no es conexo

    print_test("Pruebas Grafo, camino minimo A-C es None", not grafo.camino_minimo("A", "C"))
    print_test("Pruebas Grafo, camino minimo B-D es None", not grafo.camino_minimo("B", "D"))
    print_test("Pruebas Grafo, camino minimo F-H es None", not grafo.camino_minimo("F", "H"))

def pruebas_grafo_random_walk():
    grafo = Grafo()

    grafo.add("A")
    grafo.add("B")
    grafo.add("C")
    grafo.add("D")
    grafo.add("E")
    grafo.add("F")
    grafo.add("G")
    grafo.add("H")
    grafo.add("I")

    grafo.agregar_arista("A", "B", 4)
    grafo.agregar_arista("A", "H", 8)
    grafo.agregar_arista("B", "C", 8)
    grafo.agregar_arista("B", "H", 8)
    grafo.agregar_arista("C", "D", 7)
    grafo.agregar_arista("C", "F", 4)
    grafo.agregar_arista("C", "I", 2)
    grafo.agregar_arista("D", "E", 9)
    grafo.agregar_arista("D", "F", 14)
    grafo.agregar_arista("E", "F", 10)
    grafo.agregar_arista("F", "G", 2)
    grafo.agregar_arista("G", "I", 6)
    grafo.agregar_arista("G", "H", 1)
    grafo.agregar_arista("H", "I", 7)

    print_test("Pruebas Grafo, random walk tiene el largo correcto", len(grafo.random_walk(10, pesado = False)) == 10)
    print_test("Pruebas Grafo, random walk tiene el largo correcto", len(grafo.random_walk(10, pesado = True)) == 10)
