#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
# La línea # -*- coding: utf-8 -*- permite la utilización de un
# formato de codificación de caracteres Unicode. Esto habilita el
# uso de tildes por ejemplo, que de otra manera podrían causar
# errores.
# Se asume que el camino /opt/rh/rh-Python36/root/usr/bin/Python3.6
# es donde está Python 3.6. Este camino podría variar. También es posible
# acceder al intérprete de Python utilizando
# por ejemplo #!/usr/bin/env Python (dependiendo del caso).
# Se importa la función Popen del módulo subprocess de Python.
# Esta función permite ejecutar comandos de Linux en Python
# (permitirá ejecutar el script de la parte 1 del obligatorio).
# También se importa PIPE del módulo subprocess, para poder manejar
# la salida estándar y la salida estándar de errores del comando
# (del script del ejercicio 1).
from subprocess import Popen, PIPE
# El módulo sys es útil para poder desplegar un mensaje en la salida
# estándar de errores.
import sys
# Se define una función que recibe como parámetro un string. Este
# string tiene la misma estructura que las líneas que produce el script
# del ejercicio 1, con un largo de un camino, un separador ":", y un
# camino. La función y devuelve otro string con un largo del camino, un
# separador ":", la cantidad de directorios que tiene (sin contarse el
# propio archivo si es un directorio), un separador ":" y el camino.
# El objetivo de esta función es obtener el campo adicional pedido en
# el ejercicio 2 del obligatorio, con la cantidad de directorios, en
# base a una línea producida por el script del ejercicio 1.
# Dado la funcionalidad que se pide, para determinar la cantidad de
# directorios que tiene un camino, sin considerarse el propio archivo al
# que corresponde el camino, alcanza con contar la cantidad de
# ocurrencias del carácter "/", tanto si el camino es relativo como
# absoluto.
def agrega_directorios(largo_y_camino):
 # Separo el largo y el camino según el carácter ":".
 largo, camino = largo_y_camino.split(":")
 # Se calcula la cantidad de directorios que tiene el camino (sin
 # contar al propio archivo, si fuera un directorio).
 cant_dir = camino.count("/")
 # Se forma el string con los datos correspondientes separados por
 # el carácter ":".
 return(str(largo) + ":" + str(cant_dir) + ":" + camino)
"""
INFORMACIÓN COMPLEMENTARIA, SOLO A MODO DE EJEMPLO, USÁNDOSE EL MODULO
SYS PARA ACCEDER A LOS PARÁMETROS RECIBIDOS POR EL SCRIPT EN PYTHON.
# El módulo sys permite acceder a los parámetros recibidos por el script
# Python usando la variable sys.argv, que es una lista con los parámetros
# recibidos. Se usará el módulo argparse, por lo que estas líneas quedan
# comentadas.
import sys
print ("Número de parámetros: ", len(sys.argv))
print ("Lista de argumentos: ", sys.argv)
"""
# Se utiliza el módulo argparse para interpretar los parámetros
# recibidos por este script Python.
import argparse
parser = argparse.ArgumentParser()
# Se definen los distintos modificadores y el parámetro directorio, junto
# con el texto que los describe. Se van adicionando uno a uno.
# Se define el modificador para recursividad.
parser.add_argument("-r", "--recursivo", help="Busca los archivos en forma
recursiva a partir del directorio pasado como parámetro.",
action="store_true")
# Se define el modificador para buscar solo archivos regulares.
parser.add_argument("-f", "--arch_regulares", help="Solo busca los archivos
regulares.", action="store_true")
# Se define el modificador para buscar archivos no ocultos.
parser.add_argument("-v", "--visibles", help="Solo busca los archivos que no
sean ocultos.", action="store_true")
# Se define el modificador para considerar caminos relativos.
parser.add_argument("-l", "--local", help="Los caminos mostrados y
contabilizados se consideran relativos a partir del directorio pasado como
parámetro.", action="store_true")
# Se define el modificador para invertir el orden del listado.
parser.add_argument("-i", "--invertir", help="Invierte el orden de la
salida.", action="store_true")
# Se define el modificador para desplegar reporte al final del listado.
parser.add_argument("-t", "--totales", help="Despliega reporte con la
cantidad de archivos encontrados.", action="store_true")
# Se define el modificador para determinar el orden del listado. A su
# vez, este modificador tiene dos opciones, la "l" y la "d", definidos
# con el parámetro choices=["l", "d"].
parser.add_argument("-o", "--orden", type=str, choices=["l", "d"],
help="Ordenar la salida por largo del camino (parámetro l) o por cantidad de
subdirectorios (parámetro d).")
# Se define el parámetro directorio, que puede tener cualquier valor (no
# es un modificador).
parser.add_argument("directorio", type=str, help="Directorio donde se va a
hacer la búsqueda.")
# Se procesan los argumentos recibidos por el script en Python.
# Se captura la excepción SystemExit para poder salir con el código
# de salida que se pide en el ejercicio 2 y no con el código de salida
# que genere parser.parse_args().
try:
 args = parser.parse_args()
except SystemExit as e:
 # Se define a 10 como el código de salida en caso que se detecte
 # algún problema en los argumentos de entrada.
 exit(10)
# Sintaxis del ejercicio 1:
# ej1_largo_caminos.sh [-r] [-f] [-v] [-l] [-n] Directorio
# Se preparan el comando y los argumentos para ejecutar el script del
# ejercicio 1. Hay un claro paralelismo entre varios de los modificadores
# de este script en Python con los modificadores del script del
# ejercicio 1.
# Para ejecutar el script del ejercicio 1, se crea una lista que
# contendrá el comando a ser ejecutado y todos los argumentos que va
# a recibir. El primer elemento de esta lista determina el
# comando a ser ejecutado, y por tanto será el camino absoluto
# al script en bash del ejercicio 1 (esto permite independizarse
# del directorio corriente de trabajo).
ej1_y_lista_parametros = ['/oblgDevOps/ejercicio
1/ej1_largo_caminos_sin_getopts.sh']
# Si el usuario ha elegido la opción de buscar archivos en forma
# recursiva, entonces al ejercicio 1 hay que pasarle el modificador –r,
# y debe agregarse a la lista.
if args.recursivo:
 ej1_y_lista_parametros.append("-r")
# Si el usuario solo busca listar archivos regulares, entonces al
# ejercicio 1 hay que pasarle el modificador –f, y debe agregarse a
# la lista.
if args.arch_regulares:
 ej1_y_lista_parametros.append("-f")
# Si el usuario solo busca listar archivos no ocultos, entonces al
# ejercicio 1 hay que pasarle el modificador –v, y debe agregarse a
# la lista.
if args.visibles:
 ej1_y_lista_parametros.append("-v")
# Si el usuario quiere que los caminos a desplegarse sean relativos
# (al directorio pasado como parámetro), entonces al ejercicio 1 hay que
# pasarle el modificador –l, y debe agregarse a la lista.
if args.local:
 ej1_y_lista_parametros.append("-l")
# Si se define un orden por largo de camino, esa opción es equivalente al
# modificador -n del script del ejercicio 1 (y se le pasa ese
# modificador al script, agregándose a la lista).
if args.orden == "l":
 ej1_y_lista_parametros.append("-n")
# Como último parámetro, al script del ejercicio 1, se le pasa el
# directorio, agregándose a la lista.
ej1_y_lista_parametros.append(args.directorio)
"""
# INFORMACIÓN DE USO DE CALL (no usada para esta solución).
# Otra manera de ejecutar un comando es usar la función call. Como en
# este caso es necesario obtener también la salida estándar y salida
# estándar de errores, se usara Popen, pero se deja información de call
# como referencia aquí:
# La función call ejecuta un comando. Como resultado se obtiene el código
# de retorno del mismo.
# La función call, del módulo subprocess, recibe como parámetro una lista
# con el comando a ejecutarse (que en este caso sería el camino absoluto
# al script del ejercicio 1) y los parámetros que debe recibir el
# mismo. No se debe proteger el espacio de separación en el nombre
# "ejercicio 1", porque ya el primer elemento de la lista (la lista 
# completa es recibida como el primer parámetro de la función call)
# es el camino al comando. Si se intenta usar, por ejemplo, el camino:
# "/oblgDevOps/ejercicio\ 1/ej1_largo_caminos.sh", se generará un error.
# Esta observación también se aplica para los argumentos a pasarse al
# comando (como el camino al directorio a listarse).
# El siguiente es un ejemplo correcto de uso de call para este ejercicio:
cod_salida = call(['/oblgDevOps/ejercicio
1/ej1_largo_caminos_sin_getopts.sh', "-r", "-v", "-l", "../ejercicio 1"])
# En la variable cod_salida queda almacenado el código de retorno del
# comando ejecutado con call, con los parámetros indicados.
# FIN DE INFORMACIÓN DE USO DE CALL (no usada para esta solución).
"""
"""
# COMENTARIOS Y EJEMPLOS SOBRE EL USO DE Popen.
# Popen permite obtener la salida estándar, salida estándar de errores y
# el código de salida de un comando ejecutado.
# Sintaxis general de Popen:
# Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
# El parámetro shell=True hace que el comando sea interpretado por una
# shell. De esta forma, en vez de pasarse el comando y los argumentos
# en una lista a Popen, directamente se le pasa en un mismo string el
# comando y sus argumentos todos juntos (como si fueran escritos por un
# usuario en la línea de comandos en una terminal), para ser
# interpretados por la shell y que se produzca la ejecución. Esta
# solución se considera menos elegante y menos segura y no se usa aquí
# para el segundo ejercicio del obligatorio.
# El siguiente ejemplo muestra cómo se ejecuta ls -l .*. Si no se usa
# el parámetro de Popen shell=True, al ponerse "ls -l .*" como comando,
# causa error, pues no hay una shell que expanda el ".*", siendo además
# todo el string "ls -l .*" interpretado como el comando "ls -l .*" y no
# como el comando "ls" con el modificador "-l" y como argumentos los
# archivos ocultos del directorio corriente de trabajo.
proceso_ls = Popen("ls -l .*", shell=True, stdout = PIPE)
print("Salida del ls -l .* con uso de shell=true:")
print(proceso_ls.communicate()[0])
# El siguiente ejemplo muestra otra posibilidad, que es usar:
# proceso_ls2 = Popen(["ls", "-la"],stdout = PIPE), pero no hace
# exactamente lo mismo que el ejemplo anterior. En este caso, no es
# posible utilizar ".*", ya que no se puede expandir al no haber una
# shell interpretando el comando (por no estar el parámetro shell=True en
# Popen). Si se pusiera proceso_ls2 = Popen(["ls", ".*"],stdout = PIPE),
# entonces ".*" no sería expandido (por no haber quien haga la
# expansión de nombres) y será tomado como un literal (como el archivo de
# nombre ".*"), causando error.
proceso_ls2 = Popen(["ls", "-la"], stdout = PIPE)
print("salida del ls -la con lista de parámetros:")
print(proceso_ls2.communicate()[0])
# FIN COMENTARIOS DE USO DE Popen.
"""
# Las opciones del script del ejercicio 1 se aceptan en el siguiente
# orden -r, -f, -v, -l y –n (dado por la letra del obligatorio de ese
# ejercicio).
# Para obtener la salida estándar, la salida estándar de errores y el
# código de salida del script del ejercicio 1, se usa Popen, pasándole el
# comando con sus argumentos como una lista (cargada en la variable
# ej1_y_lista_parametros), donde el primer elemento es el comando y los
# siguientes son sus parámetros. Después de esa lista, a Popen se le
# pasa stdout = PIPE y stderr = PIPE para poder recuperar después la
# salida estándar y la salida estándar de errores.
process = Popen(ej1_y_lista_parametros, stdout = PIPE, stderr = PIPE)
# El objeto process permite ejecutar el comando solicitado y acceder a la
# información que produce. Para obtener el código de retorno, la salida
# estándar y la salida estándar de errores del script del ejercicio 1, es
# necesario ejecutar el método communicate de este objeto (este método
# causa la ejecución del ejercicio 1).
# El método communicate retorna una tupla con la salida y la entrada
# estándar (stdoutdata, stderrdata). La variable output será una tupla
# con la salida estándar como primer elemento y la salida estándar de
# errores como segundo elemento.
output = process.communicate()
# Con process.returncode se obtiene el código de retorno (exit code) del
# script del ejercicio 1.
# Si el código de retorno del script del ejercicio 1 es distinto de 0,
# entonces hay un error y por tanto hay que desplegar por la salida
# estándar de errores el mismo mensaje de error que ha devuelto ese
# script, además salir con su mismo código de error.
if process.returncode > 0:
 # Se despliega el mensaje producido por el script del ejercicio 1 por
 # la salida estándar de errores.
 # Se usa el método decode para formatear correctamente la salida para
 # ser impresa. Podría usarse en este caso también .decode('utf-8').
 print(output[1].decode(), file = sys.stderr, end="")
 # Se finaliza la ejecución del programa con el mismo código de error
 # que el script del ejercicio 1.
 exit(process.returncode)
# Se verifica si se ha recibido información por la entrada estándar de
# errores.
# Aunque no sea un error, hay que reenviar (a la salida estándar de
# errores de este programa en Python) el mensaje que genera el script del
# ejercicio 1 por su salida estándar de errores, en caso que no existan
# archivos para listar.
# Este if podría fusionarse con el if de arriba, ya que la secuencia de
# instrucciones que contiene es exactamente la misma (en este caso,
# process.returncode vale 0). Se dejan separados para que queden más
# claras las dos condiciones y poder hacer un comentario más específico.
if output[1].decode() != "":
 print(output[1].decode(), file=sys.stderr, end="")
 exit(0)
# Se genera una lista donde cada elemento es una línea producida por el
# script del ejercicio 1 (cada línea está formada por el largo del camino
# a un archivo, separador ":" y seguidamente el camino a ese archivo).
# Se utiliza al enter ("\n") para separar las líneas.
lista_archivos_ej1 = output[0].decode().split("\n")
# La anterior instrucción genera que el último elemento de la lista sea
# un elemento vacío (ya que la última línea con datos del ejercicio 1
# tiene un enter al final). Con la siguiente instrucción, se quita el
# último elemento de la lista para solucionar el problema (y no
# considerar un camino vacío).
# Para eliminar un elemento por su índice se usa pop. El índice -1
# equivale al último elemento de la lista.
lista_archivos_ej1.pop(-1)
# Se define la variable (una lista) que contendrá la información de los
# archivos, con sus largos, cantidad de directorios y los caminos, con
# esos campos separados por ":".
lista_arch_con_cant_directorios = []
# Se construye la lista que contendrá la información a desplegar por
# este programa en Python (sin considerar el orden, el cual se aplicara
# más adelante). A cada archivo listado por el script del ejercicio 1 se
# le agrega la cantidad de directorios que tiene, sin contar al propio
# archivo (si fuera un directorio).
for largo_y_camino in lista_archivos_ej1:
 lista_arch_con_cant_directorios.append(agrega_directorios(
largo_y_camino))
# Si se ha recibido el parámetro d del modificador -o (el usuario ingresa #
en la línea de comandos -o d), entonces hay que ordenar los caminos por
# la cantidad de directorios que tienen, en forma descendente.
if args.orden == "d":
 # Se aplica el orden usando una función lambda. En este caso, esta
 # función retorna el campo que debe tenerse en cuenta para el
 # ordenamiento (que es el segundo), donde está la cantidad de
 # directorios que tiene el camino (sin contarse al propio archivo,
 # si es un directorio).
 # La función lambda se asocia al parámetro key, lo que permite
 # definir los valores a ser usados para el ordenamiento (estos
 # valores determinarán el orden de los elementos de la lista). En
 # esta solución, la función lambda está retornando el segundo campo,
 # convertido a tipo entero, de un elemento de la lista (la función
 # lambda se aplicará a cada elemento de la lista en el proceso de
 # ordenamiento). El uso de info_archivo.split(":")[1]permite obtener
 # el segundo campo de cada elemento de la lista (teniendo en cuenta
 # que info_archivo.split(":")[0] es el primero) y con
 # int(info_archivo.split(":")[1]) se pasan a entero, para que el
 # ordenamiento aplicado sea numérico (y no de texto). La conversión a
 # entero es muy importante, porque de lo contrario se tomará un orden
 # alfabético de esos valores, ya que el segundo campo de cada
 # elemento de la lista es de tipo string (pues es una parte de un
 # string), siendo ordenados como texto por defecto (si no fueran
 # pasados a int). Esto puede causar problemas en el orden, haciendo
 # que, por ejemplo, el valor 150 sea considerado menor que el 2, ya
 # que si bien 150 es mayor a 2 como valor entero, es menor a 2 como
 # string (así como "alamo" es menor a "x" y cualquier número que
 # comience con 1, como el 150, es menor a cualquiera que empiece
 # con 2).
 # El parámetro reverse = True indica que el orden se invertirá,
 # para que queden los caminos con la mayor cantidad de directorios
 # primero (el orden por defecto es creciente y no decreciente,
 # por eso es necesario usar reverse para cambiarlo).
 lista_arch_con_cant_directorios.sort(key = lambda info_archivo:
int(info_archivo.split(":")[1]), reverse = True)
# Se comprueba si el usuario ha solicitado invertir el orden definido por
# defecto. En caso que se tenga que invertir, se le aplica orden inverso
# a la lista usándose el método reverse.
# Puede suceder que en la anterior instrucción (el if anterior) se
# invierta el orden de la lista (usándose reverse = True) y aquí también
# se aplique un orden invertido. Esta doble inversión sucede en el caso
# que el usuario solicite invertir el orden de los registros y además
# pida simultáneamente ordenar los caminos por la cantidad de
# directorios que tienen (haciendo que las condiciones de este if y
# también del anterior sean verdaderas). Con un testeo diferente
# de los parámetros del usuario, estas inversiones podrían simplificarse
# y no hacerse (ya que se anulan entre sí), para el caso de recibirse
# como modificadores –o d y –i. Sin embargo, eso haría menos clara la
# lógica de procesamiento de los modificadores ingresados por el
# usuario y menos simple este programa en Python, prefiriéndose esta
# solución (menos eficiente en tiempo de ejecución en el caso de
# recibirse –o d y –i, pero más eficiente en líneas de código y
# legibilidad).
if args.invertir:
 lista_arch_con_cant_directorios.reverse()
# Se despliega la lista (que ya está ordenada como ha solicitado el
# usuario) con la información de los archivos (para cada archivo: largo
# del camino, cantidad de directorios y el camino).
for info_archivo in lista_arch_con_cant_directorios:
 print(info_archivo)
# Si el usuario pide mostrar la cantidad de archivos listada, se
# despliega la información solicitada.
if args.totales:
 # Se comienza el string con un \n para que quede una línea de
 # separación con la salida anterior (la lista de archivos).
 print("\nSe han desplegado {}
archivos".format(len(lista_arch_con_cant_directorios)))
# El exit en realidad no es necesario, ya que está terminando el
# programa. Por defecto se retorna con código de retorno 0.
exit()