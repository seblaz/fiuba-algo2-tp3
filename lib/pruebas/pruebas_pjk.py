from lib.grafo import Grafo
from lib.pjk import Pjk
from lib.pruebas.testing import *

def run(pruebas_volumen = 100):
    pruebas_pjk()

def pruebas_pjk():
    grafo = Grafo()
    pjk = Pjk("marvel.pjk", grafo)

    print_test("Pruebas Pjk, el grafo no tiene elementos", len(grafo) == 0)

    pjk.leer()
    pjk.cerrar()

    print_test("Pruebas Pjk, la cantidad de elementos es correcta", len(grafo) == 6411)
