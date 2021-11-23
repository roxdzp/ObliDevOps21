
#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

import sys

import argparse

import re

ej1_last = ['/root/ObliDevOps21/ej1Obligatorio.sh']

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--recuento_horas", help="Devuelve un contador de las horas/minutos/dias sumadas.", action="store_true")

parser.add_argument("-u", "--usuario", type=str, default="", help="Nos permite buscar las horas de un usuario en particular, va a compañado de una variable que es el nombre de usuario.")

parser.add_argument("-o", "--orden", type=str, choices=["u", "t", "h", "d"], help="Ordenar de forma creciente la salida del LAST por una de las cuatro columnas a seleccionar.")

parser.add_argument("-f", "--filtro", type=str, choices=["u", "t", "h", "f", "c", "n", "d"], help="Filtrado de listado (quita opciones).", nargs='+')

parser.add_argument("-i", "--inverso", help="Devuelve el listado de los valores ordenados con el -o pero de forma inversa.", action="store_true")

try:
    args = parser.parse_args()
except SystemExit as e:
    print("Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.")
    exit(25)

if args.recuento_horas:
    ej1_last.append("-r")

if args.usuario:
    ej1_last.append("-u")
    ej1_last.append(args.usuario)

process = Popen(ej1_last, stdout = PIPE, stderr = PIPE)

output = process.communicate()

if process.returncode > 0:
    print(output[1].decode(), file = sys.stderr, end="")
    exit(process.returncode)

if output[1].decode() != "":
    print(output[1].decode(), file=sys.stderr, end="")
    exit(0)

## Creamos una función que en base a los cabezales de siempre, y a una lista, nos imprime esa lista con los cabezales.
## La variable valores_sumados la recibe al ser llamada y tiene en ella el valor de los valores sumados al haberse ingresado -r

#Los valores en la lista_normalizada son en base a la columna:
#1=-u=usuario
#2=-t=terminal
#3=-h=host
#4-6=-f=fecha de conexión
#7=-h=hora de conexión
#8=-=el guion-
#9=-n=hora de desconexión
#10=-d=tiempo total de conexion

def normalizar_lista():
    ## Guardamos en una lista todas las lineas de la salida estandar del script de bash
    lista=output[0].decode().split("\n")
    headers='Usuario Term Host Fecha - - H.Con - H.Des T.Con'
    ## Guardamos los cabezales en una variable
    if args.recuento_horas :
        suma_valores=lista[-2]
        lista_normalizada=[]
        lista_normalizada.append(headers)
        for i in range(1,len(lista)-2):
            if lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores
    else:
        suma_valores=""
        lista_normalizada=[]
        lista_normalizada.append(headers)
        for i in range(1,len(lista)):
            if lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores
    ## Previo a poder trabajar con los resultados de la lista que tenemos, la normalizamos quitando los espacios repetidos y convirtiendolos
    ## en solo un espacio y eliminando todas las lineas que inicien con reboot, para trabajar unicamente con usuarios.

## Creamos una función que nos permita filtrar por una columna en particular del LAST recibido.
def filtrar_last(opcion, lista_filtrada):
    lista_filtrada.pop(-1)
    indice=0
    if opcion == "u" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Usuario':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    if opcion == "t" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Term':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    elif opcion == "h" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Host':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    elif opcion == "f" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Fecha':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        for fila in lista_filtrada:
            fila.pop(indice)
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    elif opcion == "c" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'H.Con':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    elif opcion == "n" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'H.Des':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada
    elif opcion == "d" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'T.Con':
                indice=i
        for fila in lista_filtrada:
            fila.pop(indice)
        return lista_filtrada

global lista_filtrada
lista_filtrada=[]
if args.filtro != None:
    for i in args.filtro:
        if i == "u":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("u",lista_filtrada) 
            else:
                lista_filtrada=filtrar_last("u",lista_filtrada)
        elif i == "t":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("t",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("t",lista_filtrada)
        elif i == "h":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("h",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("h",lista_filtrada)
        elif i == "f":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("f",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("f",lista_filtrada)
        elif i == "n":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("n",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("n",lista_filtrada)
        elif i == "c":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("c",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("c",lista_filtrada)
        elif i == "d":
            if len(lista_filtrada) == 0:
                lista = normalizar_lista()
                for i in range(0,len(lista[0])):
                    lista_filtrada.append(lista[0][i].split(" "))
                lista_filtrada=filtrar_last("d",lista_filtrada)
            else:
                lista_filtrada=filtrar_last("d",lista_filtrada)

#print("lista filtrada",lista_filtrada)


def ordenar_last(opcion,invertido,lista_normalizada):
    cabezales=lista_normalizada[0]
    indice=0
    contador=0
    if opcion == "u" :
        for i in lista_normalizada[0].split(" "):
            contador=contador+1
            if i == 'Usuario':
                indice=contador-1
        print("---------------------------")
        print("Ordenar por usuario:\n")
        lista_normalizada=sorted(lista_normalizada, key=lambda x: x.split(" ")[indice], reverse=invertido)
        return lista_normalizada,cabezales
    elif opcion == "t" :
        for i in lista_normalizada[0].split(" "):
            contador=contador+1
            if i == 'Term':
                indice=contador-1
        print("---------------------------")
        print("Ordenar por Terminal:\n")
        lista_normalizada.pop(0)
        lista_normalizada.pop(-1)
        lista_normalizada=sorted(lista_normalizada, key=lambda x: x.split(" ")[indice], reverse=invertido)
        return lista_normalizada,cabezales
    elif opcion == "h" :
        for i in lista_normalizada[0].split(" "):
            contador=contador+1
            if i == 'Host':
                indice=contador-1
        print("---------------------------")
        print("Ordenar por host:")
        lista_normalizada.pop(0)
        lista_normalizada.pop(-1)
        lista_normalizada=sorted(lista_normalizada, key=lambda x: x.split(" ")[indice], reverse=invertido)
        return lista_normalizada,cabezales
    elif opcion == "d" :
        for i in lista_normalizada[0].split(" "):
            contador=contador+1
            if i == 'T.Con':
                indice=contador-1
        print("---------------------------")
        print("Ordenar por duracion de conexion:")
        lista_normalizada.pop(0)
        lista_normalizada.pop(-1)
        lista_normalizada=sorted(lista_normalizada, key=lambda x: x.split(" ")[indice].replace("(","").replace(")","").replace(":",""), reverse=invertido)
        return lista_normalizada,cabezales

global lista_normalizada
lista_normalizada=[]
if len(lista_filtrada) == 0:
    lista_filtrada=normalizar_lista()
    lista_normalizada=lista_filtrada[0]
else:
    for i in lista_filtrada:
        linea=""
        for j in range(0,len(i)):
            linea=linea+" "+i[j]
        lista_normalizada.append(linea)

inverso=False
if args.inverso:
    inverso=True
else:
    inverso=False

if args.orden == "u":
    lista_normalizada=ordenar_last("u",inverso, lista_normalizada)
elif args.orden == "t":
    lista_normalizada=ordenar_last("t",inverso, lista_normalizada)
elif args.orden == "h":
    lista_normalizada=ordenar_last("h",inverso, lista_normalizada)
elif args.orden == "d":
    lista_normalizada=ordenar_last("d",inverso, lista_normalizada)


## Creamos una función que recibe la opción del parametro -o el cual nos dira como organizar la lista normalizada.

## La opción inverso nos permite valdiar si el listado va a ser mostrado de forma inversa o no.
## Al pasar la variable inverso que es de tipo boolean a la funcion ordenar_last luego podemos definir si el 
## reverse=true o reverse=false con un reverse=inverso
## Además nos permite validar si utilizamos la sumatoria de valores del -r con el atributo -i para poder invertir esta lista
## Otra cosa que podemos hacer es que si solo se introduce -i, podemos invertir la lista del LAST recibido por la salida estandar
## del script de bash.

## Si la persona ingresa -r (recuento_horas) y -i (inverso), lo que se hace es guardar el resultado del bash en una lista
## y luego lo que hacemos es imprimir cada linea, de atrás para adelante, pero eliminando las ultimas 3 lineas 
## (espacio-sumatoria-espacio), y terminamos en el 1 para evitar los cabezales.
## Al finalizar, si la opción -i esta seleccionada, entonces hacemos un print de la lista[-2] que es la sumatoria de datos al final.
if args.orden:
    for j in range(0,len(lista_normalizada[0])):
        print(lista_normalizada[0][j])
    print("\n")
    exit(0)
elif args.recuento_horas and inverso == False :
    
    lista=normalizar_lista()
    for j in range(0,len(lista_normalizada)):
        print(lista_normalizada[j])
    print("\n")
    print(lista[1])
    exit(0)
elif args.recuento_horas and inverso:
    
    lista=normalizar_lista()
    if len(lista_normalizada) != 0:
        for j in range(len(lista_normalizada)-1, 1, -1):
            print(lista_normalizada[j])
    else:
        for j in range(len(lista_normalizada)-1, 1, -1):
            print(lista_normalizada[j])
    print("\n")
    print(lista[1])
    exit(0)
else: 
    lista=normalizar_lista()
    for j in range(0,len(lista_normalizada)):
        print(lista_normalizada[j])
    print("\n")
    exit(0)