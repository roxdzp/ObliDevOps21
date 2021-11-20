#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

import sys

ej1_y_lista_parametros = ['/root/ObliDevOps21/ej1Obligatorio.sh']

ej1_y_lista_parametros.append("-r")

ej1_y_lista_parametros.append("-u")

ej1_y_lista_parametros.append("root")

process = Popen(ej1_y_lista_parametros, stdout = PIPE, stderr = PIPE)

output = process.communicate()

print(output[0].decode(), file = sys.stderr, end="")

