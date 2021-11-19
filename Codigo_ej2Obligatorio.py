from subprocess import Popen, PIPE

import sys

def agrega_directorios(largo_y_camino):
    largo, camino = largo_y_camino.split(":")
    cant_dir = camino.count("/")
    return(str(largo) + ":" + str(cant_dir) + ":" + camino)

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--arch_regulares", help="Solo busca los archivos regulares.", action="store_true")

parser.add_argument("-v", "--visibles", help="Solo busca los archivos que no sean ocultos.", action="store_true")

parser.add_argument("-l", "--local", help="Los caminos mostrados y contabilizados se consideran relativos a partir del directorio pasado como parámetro.", action="store_true")

parser.add_argument("-o", "--orden", type=str, choices=["l", "d"], help="Ordenar la salida por largo del camino (parámetro l) o por cantidad de subdirectorios (parámetro d).")

try:
    args = parser.parse_args()
except SystemExit as e:
    exit(10)

ej1_y_lista_parametros = ['/oblgDevOps/ejercicio1/ej1_largo_caminos_sin_getopts.sh']

if args.local:
    ej1_y_lista_parametros.append("-l")

if args.orden == "l":
    ej1_y_lista_parametros.append("-n")

ej1_y_lista_parametros.append(args.directorio)

process = Popen(ej1_y_lista_parametros, stdout = PIPE, stderr = PIPE)

output = process.communicate()

if process.returncode > 0:
    print(output[1].decode(), file = sys.stderr, end="")
    exit(process.returncode)

if output[1].decode() != "":
    print(output[1].decode(), file=sys.stderr, end="")
    exit(0)

lista_archivos_ej1 = output[0].decode().split("\n")

lista_archivos_ej1.pop(-1)

lista_arch_con_cant_directorios = []

exit()