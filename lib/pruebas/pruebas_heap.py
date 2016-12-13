from lib.heap import Heap
from lib.pruebas.testing import *
import time, random

def run(pruebas_volumen = 100):
    print("~ Pruebas Heap ~")
    # pruebas_heap_vacio()
    # pruebas_heap_un_elemento()
    # pruebas_heap_varios_elementos()
    # pruebas_heap_actualizar_prioridad()

def pruebas_heap_vacio():
    heap = Heap()
    print_test("Pruebas Heap, el heap no es None", heap is not None)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
    print_test("Pruebas Heap, la cantidad de elementos es cero", len(heap) == 0)
    # print_test("Pruebas Heap, el heap no contiene elementos", "test" not in heap)
    print_exception(heap.popitem, IndexError, "Pruebas Heap, eliminar un elemento lanza IndexError")

def pruebas_heap_un_elemento():
    heap = Heap()
    var = "iron"
    heap[var] = 0
    print_test("Pruebas Heap, el heap no es None", heap is not None)
    print_test("Pruebas Heap, la cantidad de elementos es uno", len(heap) == 1)
    # print_test("Pruebas Heap, el heap contiene a 'var'", var in heap)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    print_test("Pruebas Heap, eliminar un elemento del heap es 'var'", heap.popitem() == (var, 0))
    print_test("Pruebas Heap, despues de elminar 'var' la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
    # print_test("Pruebas Heap, despues de elminar 'var' el heap no contiene a 'var'", var not in heap)

def pruebas_heap_varios_elementos():
    heap = Heap()
    vars = {0:"iron", 1:"maiden", 2:"black", 3:"sabbath"}
    for prioridad, valor in vars.items():
        heap[valor] = prioridad

    print_test("Pruebas Heap, la cantidad de elementos es 4", len(heap) == 4)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    # for valor in vars.values():
        # ok = valor in heap
        # if not ok: break
    # print_test("Pruebas Heap, el heap contiene a todas las variables", ok)

    for x in range(4):
        ok = heap.popitem() == (vars[x], x)
        if not ok: break
    print_test("Pruebas Heap, el heap elimino los elementos en orden", ok)
    print_test("Pruebas Heap, despues de elminar 'var' la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())

def pruebas_heap_actualizar_prioridad():
    heap = Heap()
    heap["iron"]    = 2
    heap["maiden"]  = 4
    heap["black"]   = 3
    heap["sabbath"] = 1
    heap["sabbath"] = 6

    print_test("Pruebas Heap, eliminar un elemento del heap ok", heap.popitem() == ("iron", 2))
    print_test("Pruebas Heap, eliminar un elemento del heap ok", heap.popitem() == ("black", 3))
    print_test("Pruebas Heap, eliminar un elemento del heap ok", heap.popitem() == ("maiden", 4))
    print_test("Pruebas Heap, eliminar un elemento del heap ok", heap.popitem() == ("sabbath", 6))

def pruebas_heap_volumen(cantidad_pruebas):
    heap = Heap()
    dicc = {}
    for x in range(cantidad_pruebas):
        dicc[x] = random.random()
        heap[x] = dicc[x]

    print_test("Pruebas Heap, la cantidad de elementos es correcta", len(heap) == cantidad_pruebas)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    for x in range(cantidad_pruebas):
        elem = heap.popitem()
        ok = dicc[elem[0]] == elem[1]
        if not ok: break
    print_test("Pruebas Heap, el heap elimino los elementos en orden", ok)
    print_test("Pruebas Heap, la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
