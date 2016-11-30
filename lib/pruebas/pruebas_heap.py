from lib.heap import Heap
from lib.pruebas.testing import *

def run(pruebas_volumen = 100):
    print("~ Pruebas Heap ~")
    pruebas_heap_vacio()
    pruebas_heap_un_elemento()
    pruebas_heap_varios_elementos()
    pruebas_heap_volumen(pruebas_volumen)

def pruebas_heap_vacio():
    heap = Heap()
    print_test("Pruebas Heap, el heap no es None", heap is not None)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
    print_test("Pruebas Heap, la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap no contiene elementos", "test" not in heap)
    print_exception(heap.pop, IndexError, "Pruebas Heap, eliminar un elemento lanza IndexError")

def pruebas_heap_un_elemento():
    heap = Heap()
    var = "iron"
    heap[0] = var
    print_test("Pruebas Heap, el heap no es None", heap is not None)
    print_test("Pruebas Heap, la cantidad de elementos es uno", len(heap) == 1)
    print_test("Pruebas Heap, el heap contiene a 'var'", var in heap)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    print_test("Pruebas Heap, eliminar un elemento del heap es 'var'", heap.pop() == var)
    print_test("Pruebas Heap, despues de elminar 'var' la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
    print_test("Pruebas Heap, despues de elminar 'var' el heap no contiene a 'var'", var not in heap)

def pruebas_heap_varios_elementos():
    heap = Heap()
    vars = {0:"iron", 1:"maiden", 2:"black", 3:"sabbath"}
    for prioridad, valor in vars.items():
        heap[prioridad] = valor

    print_test("Pruebas Heap, la cantidad de elementos es 4", len(heap) == 4)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    for valor in vars.values():
        ok = valor in heap
        if not ok: break
    print_test("Pruebas Heap, el heap contiene a todas las variables", ok)

    for x in range(4):
        ok = heap.pop() == vars[x]
        if not ok: break
    print_test("Pruebas Heap, el heap elimino los elementos en orden", ok)
    print_test("Pruebas Heap, despues de elminar 'var' la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())

def pruebas_heap_volumen(cantidad_pruebas):
    heap = Heap()
    for x in range(cantidad_pruebas):
        heap[x] = x

    print_test("Pruebas Heap, la cantidad de elementos es correcta", len(heap) == cantidad_pruebas)
    print_test("Pruebas Heap, el heap no esta vacio", not heap.esta_vacia())

    for x in range(cantidad_pruebas):
        ok = heap.pop() == x
        if not ok: break
    print_test("Pruebas Heap, el heap elimino los elementos en orden", ok)
    print_test("Pruebas Heap, la cantidad de elementos es cero", len(heap) == 0)
    print_test("Pruebas Heap, el heap esta vacio", heap.esta_vacia())
