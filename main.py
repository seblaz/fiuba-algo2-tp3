#!/usr/bin/python3
from lib.pruebas import pruebas_cola
from lib.pruebas import pruebas_heap
from lib.pruebas import pruebas_grafo
from lib.pruebas import pruebas_pjk
from lib.pruebas import testing
import argparse
import time

from lib.grafo import Grafo
from lib.pjk import Pjk
from lib.comandos import Comandos

parser = argparse.ArgumentParser(description='Comandos de la red social de Marvel.')
parser.add_argument('-p', '--pruebas', help='Ejecuta las pruebas', action="store_true")
parser.add_argument('-s', '--similares', nargs='+', help='Dado un personaje, encuentra los personajes más similares a este.', action='store')
parser.add_argument('-r', '--recomendar', nargs='+', help='Dado un personaje con el cual se quiere realizar un nuevo comic, recomendar otro (u otros) personaje con el cual no haya participado aún en un comic, y sea lo más similar a él posible.', action='store')
parser.add_argument('-c', '--camino', nargs='+', help='Camino más corto en tiempo para llegar desde el Personaje1 al Personaje2.', action='store')
parser.add_argument('-cen', '--centralidad', type=int, help='Permite obtener los personajes más centrales de la red. Los personajes más centrales suelen ser a su vez los más importantes (o lo que se dice en redes sociales, influyente).', action='store')
parser.add_argument('-m', '--minimo', nargs='+', help='Dijkstra', action='store')

args = parser.parse_args()
if args.pruebas:
    # pruebas_cola.run()
    # pruebas_heap.run()
    pruebas_grafo.run()
    # pruebas_pjk.run()
else:
    grafo = Grafo()
    pjk = Pjk("marvel.pjk", grafo)
    pjk.leer()
    pjk.cerrar()
    comando = Comandos(grafo)

    start_time = time.time()
    if args.similares:
        vertice = args.similares[0]
        for arg in args.similares[1:]:
            if ',' == arg[-1]:
                vertice+=" "+arg[:-1]
                break
            vertice+=" "+arg
        cantidad = int(args.similares[-1])
        print(", ".join(comando.similares(vertice, cantidad)))

    if args.recomendar:
        vertice = args.recomendar[0]
        for arg in args.recomendar[1:]:
            if ',' == arg[-1]:
                vertice+=" "+arg[:-1]
                break
            vertice+=" "+arg
        cantidad = int(args.recomendar[-1])
        print(", ".join(comando.recomendar(vertice, cantidad)))

    if args.camino:
        params = [args.camino[0], '']
        pos = 0
        for arg in args.camino[1:]:
            if ',' == arg[-1]:
                params[pos]+=' '+arg[:-1]
                pos = 1
                continue
            params[pos]+=' '+arg
        # grafo.sssp(params[0])
        print(comando.camino(params[0], params[1][1:]))
        # print(" -> ".join(comando.camino(params[0], params[1][1:])))

    if args.centralidad:
        print(args.centralidad)
        comando.centralidad(args.centralidad)

    if args.minimo:
        print(args.minimo)
        comando.grafo.sssp(' '.join(args.minimo))

    print("--- %s seconds ---" % (time.time() - start_time))

if testing.failure_count() != 0: raise Exception("Fallaron las pruebas")
