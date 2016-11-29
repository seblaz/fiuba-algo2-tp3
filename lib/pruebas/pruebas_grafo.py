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
    # print(padre.items())
    # print(orden.items())
    # en bfs el arbol de orden debe ser igual para cualquier caso
    print_test("Pruebas Grafo, bfs ok", orden["A"] == 0)
    print_test("Pruebas Grafo, bfs ok", orden["B"] == 1)
    print_test("Pruebas Grafo, bfs ok", orden["C"] == 1)
    print_test("Pruebas Grafo, bfs ok", orden["D"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["E"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["G"] == 2)
    print_test("Pruebas Grafo, bfs ok", orden["F"] == 3)
    # padre, orden = grafo.dfs("A")
    #
    # print(padre.items())
    # print(orden.items())

def pruebas_grafo_transpuesto():
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
    # grafo.agregar_arista("G", "C")

    comp_conx = grafo.componentes_conexas()
    print_test("Pruebas Grafo, componentes conexas ok", ["G","F"] or ["F","G"] in comp_conx)
