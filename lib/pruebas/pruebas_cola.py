from lib.cola import Cola
from lib.pruebas.testing import *

def run(pruebas_volumen = 100):
    print("~ Pruebas Cola ~")
    pruebas_cola_vacia()
    pruebas_cola_none()
    pruebas_cola_un_elemento()
    pruebas_cola_varios_elementos(pruebas_volumen)

def pruebas_cola_vacia():
    cola = Cola()
    print_test("Pruebas Cola, la cola no es None", cola is not None)
    print_test("Pruebas Cola, la cola esta vacia", cola.esta_vacia())
    print_test("Pruebas Cola, la cantidad de elementos es 0", len(cola) == 0)
    print_test("Pruebas Cola, cola ver_primero es None", cola.ver_primero() is None)
    print_exception(cola.desencolar, IndexError, "Pruebas Cola, desencolar cola vacia lanza IndexError")

def pruebas_cola_none():
    cola = Cola()
    cola.encolar(None)
    print_test("Pruebas Cola, la cola no es None", cola is not None)
    print_test("Pruebas Cola, la cola no esta vacia", not cola.esta_vacia())
    print_test("Pruebas Cola, la cantidad de elementos es 1", len(cola) == 1)
    print_test("Pruebas Cola, cola ver_primero es None", cola.ver_primero() is None)
    print_test("Pruebas Cola, cola desencolar es None", cola.desencolar() is None)
    print_exception(cola.desencolar, IndexError, "Pruebas Cola, desencolar cola vacia lanza IndexError")

def pruebas_cola_un_elemento():
    cola = Cola()
    var = "perro"
    cola.encolar(var)
    print_test("Pruebas Cola, la cola no es None", cola is not None)
    print_test("Pruebas Cola, la cola no esta vacia", not cola.esta_vacia())
    print_test("Pruebas Cola, la cantidad de elementos es 1", len(cola) == 1)
    print_test("Pruebas Cola, cola ver_primero es 'var'", cola.ver_primero() == var)
    print_test("Pruebas Cola, cola desencolar es 'var'", cola.desencolar() == var)
    print_exception(cola.desencolar, IndexError, "Pruebas Cola, desencolar cola vacia lanza IndexError")

def pruebas_cola_varios_elementos(cantidad_pruebas):
    cola = Cola()
    lista = list(range(0, cantidad_pruebas))
    for i in range(0, cantidad_pruebas):
        cola.encolar(lista[i])

    print_test("Pruebas Cola, encolar varios elementos, la cola no es None", cola is not None)
    print_test("Pruebas Cola, encolar varios elementos, la cola no esta vacia", not cola.esta_vacia())
    print_test("Pruebas Cola, encolar varios elementos, la cantidad de elementos es correcta", len(cola) == cantidad_pruebas)

    for i in range(0, cantidad_pruebas):
        ok  = cola.ver_primero() == i
        ok2 = cola.desencolar() == i
        ok3 = len(cola) == cantidad_pruebas-1-i
        if not (ok or ok2 or ok3): break

    print_test("Pruebas Cola, desencolar varios elementos, ver primero ok", ok)
    print_test("Pruebas Cola, desencolar varios elementos, elementos ok", ok2)
    print_test("Pruebas Cola, desencolar varios elementos, cantidad de elementos ok", ok3)
    print_test("Pruebas Cola, desencolar varios elementos, la cola esta vacia", cola.esta_vacia)
    print_test("Pruebas Cola, desencolar varios elementos, la cantidad de elementos es cero", len(cola) == 0)
