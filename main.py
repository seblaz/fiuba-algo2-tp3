#!/usr/bin/python3
# import argparse
from lib.pruebas import pruebas_cola
from lib.pruebas import pruebas_heap
from lib.pruebas import pruebas_grafo
from lib.pruebas import testing

pruebas_cola.run()
pruebas_heap.run()
pruebas_grafo.run()

if testing.failure_count() != 0: raise Exception("Fallaron las pruebas")
