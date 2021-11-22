
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

parser.add_argument("-f", "--filtro", type=str, choices=["u", "t", "h", "f", "c", "n", "d"], help="Filtrado de listado (quita opciones).")

parser.add_argument("-i", "--inverso", help="Devuelve el listado de los valores ordenados con el -o pero de forma inversa.", action="store_true")

try:
    args = parser.parse_args()
except SystemExit as e:
    print("Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.")
    exit(25)


print("**********************************************")
print("*                                                                  *")
print("*                Manual del Usuario                  *")
print("*                                                                  *")
print("**********************************************")
print(" ")
print("Modificador -o: ordenará la salida por uno de cuatro posibles criterios en forma creciente.")
print(" - Opción u: Ordenará el listado de conexiones por el nombre del usuario en forma alfabética creciente.")
print(" - Opción t: Ordenará el listado de conexiones por la terminal en orden alfabético creciente.")
print(" - Opción h: Ordenará el listado de conexiones por el host en orden alfabético creciente.")
print(" - Opción b: Ordenará el listado de conexiones por la duración de la conexión en forma creciente.") 
print("Nota: Con más de una opción de ordenamiento, se considerará la que se ingresó último y se ignorará la o las demás.")
print(" ")
print("Modificador -i: Invierte el orden del listado, se puede combinar con el Modificador -o.")
print(" ")
print("Modificador -f:  Filtrado de listado (quita opciones).")
print(" - Opción u: Quita el campo que contiene al nombre de usuario del listado.")
print(" - Opción t: Quita el campo que contiene a la terminal del listado.")
print(" - Opción h: Quita el campo que contiene el host del listado.")
print(" - Opción f: Quita el campo fecha del listado.")
print(" - Opción c: Quita el campo que contiene la hora de conexión.")
print(" - Opción n: Quita el campo que contiene la hora de desconexión.")
print(" - Opción d: Quita el campo que contiene la duración de la conexión.")
print("**********************************************")
print("\n")



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
def print_list(cabezales, lista, valores_sumados):
    ## Imprimimos los cabezales (headers)
    print(cabezales)
    for i in range(0,len(lista)):
        print(lista[i])
    print("\n")
    print(valores_sumados)

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
    ## Guardamos los cabezales en una variable
    cabezales=lista[0]
    suma_valores=lista[-2]
    ## Previo a poder trabajar con los resultados de la lista que tenemos, la normalizamos quitando los espacios repetidos y convirtiendolos
    ## en solo un espacio y eliminando todas las lineas que inicien con reboot, para trabajar unicamente con usuarios.
    lista_normalizada=[]
    for i in range(1,len(lista)-3):
        if lista[i].split(" ")[0] != "reboot" :
            lista_normalizada.append(re.sub(' +', ' ', lista[i]))
    return lista_normalizada, cabezales, suma_valores

## Creamos una función que nos permita filtrar por una columna en particular del LAST recibido.
def filtrar_last(opcion,invertido):
    lista_normalizada, cabezales, suma_valores = normalizar_lista()
    if opcion == "u" :
        print("---------------------------")
        print("Filtrar por usuario:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[1:])
        print("Term    HOST            Fecha   H.Con   H.Des   T.Con")
        for i in lista_filtrada:
            if i[1] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5])
        print(suma_valores)
    elif opcion == "t" :
        print("---------------------------")
        print("Filtrar por terminal:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[0:1]+lista_normalizada[i].split(" ")[2:])
        print("Usuario HOST            Fecha   H.Con   H.Des   T.Con")
        for i in lista_filtrada:
            if i[1] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5])
        print(suma_valores)
    elif opcion == "h" :
        print("---------------------------")
        print("Filtrar por host:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[0:2]+lista_normalizada[i].split(" ")[3:])
        print("Usuario Term    Fecha   H.Con   H.Des   T.Con")
        for i in lista_filtrada:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5])
        print(suma_valores)
    elif opcion == "f" :
        print("---------------------------")
        print("Filtrar por fecha:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[0:3]+lista_normalizada[i].split(" ")[6:])
        print("Usuario Term    HOST            H.Con   -       H.Des   T.Con")
        for i in lista_filtrada:
            if i[2] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6])
        print(suma_valores)
    elif opcion == "c" :
        print("---------------------------")
        print("Filtrar por hora de conexion:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[0:6]+lista_normalizada[i].split(" ")[8:])
        print("Usuario Term    HOST            Fecha                   H.Des   T.Con")
        for i in lista_filtrada:
            if i[2] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7])
        print(suma_valores)
    elif opcion == "n" :
        print("---------------------------")
        print("Filtrar por hora de desconexion:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[0:7]+lista_normalizada[i].split(" ")[9:])
        print("Usuario Term    HOST            Fecha                   H.Con   T.Con")
        for i in lista_filtrada:
            if i[2] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7])
        print(suma_valores)
    elif opcion == "d" :
        print("---------------------------")
        print("Filtrar por hora de conexion:\n")
        lista_filtrada=[]
        for i in range(0,len(lista_normalizada)):
            lista_filtrada.append(lista_normalizada[i].split(" ")[:10])
        print("Usuario Term    HOST            Fecha                   H.Con   -       H.Des")
        for i in lista_filtrada:
            if i[2] == "tty2":
                print(i[0]+"\t"+i[1]+"\t\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7]+"\t"+i[8])
            else:
                print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6]+"\t"+i[7]+"\t"+i[8])
        print(suma_valores)


#print("Usuario Term    HOST            Fecha   H.Con   H.Des   T.Con")

## Creamos una función que recibe la opción del parametro -o el cual nos dira como organizar la lista normalizada.
def ordenar_last(opcion,invertido):
    lista_normalizada, cabezales, suma_valores = normalizar_lista()
    if opcion == "u" :
        print("---------------------------")
        print("Ordenar por usuario:\n")
        lista_ordenada_usuario=sorted(lista_normalizada, key=lambda x: x.split(" ")[0], reverse=invertido)
        print_list(cabezales,lista_ordenada_usuario,suma_valores)
    elif opcion == "t" :
        print("---------------------------")
        print("Ordenar por terminal:\n")
        lista_ordenada_terminal=sorted(lista_normalizada, key=lambda x: x.split(" ")[1], reverse=invertido)
        print_list(cabezales,lista_ordenada_terminal,suma_valores)
    elif opcion == "h" :
        print("---------------------------")
        print("Ordenar por host:")
        lista_ordenada_host=sorted(lista_normalizada, key=lambda x: x.split(" ")[2].replace(":",""), reverse=invertido)
        print_list(cabezales,lista_ordenada_host,suma_valores)
    elif opcion == "d" :
        print("---------------------------")
        print("Ordenar por duracion de conexion:")
        lista_ordenada_duracion=sorted(lista_normalizada, key=lambda x: x.split(" ")[9].replace("(","").replace(")","").replace(":",""), reverse=invertido)
        print_list(cabezales,lista_ordenada_duracion,suma_valores)

## La opción inverso nos permite valdiar si el listado va a ser mostrado de forma inversa o no.
## Al pasar la variable inverso que es de tipo boolean a la funcion ordenar_last luego podemos definir si el 
## reverse=true o reverse=false con un reverse=inverso
## Además nos permite validar si utilizamos la sumatoria de valores del -r con el atributo -i para poder invertir esta lista
## Otra cosa que podemos hacer es que si solo se introduce -i, podemos invertir la lista del LAST recibido por la salida estandar
## del script de bash.
inverso=False
if args.inverso:
    inverso=True
else:
    inverso=False

if args.orden == "u":
    ordenar_last("u",inverso)
elif args.orden == "t":
    ordenar_last("t",inverso)
elif args.orden == "h":
    ordenar_last("h",inverso)
elif args.orden == "d":
    ordenar_last("d",inverso)
elif args.filtro == "u":
    filtrar_last("u",inverso)
elif args.filtro == "t":
    filtrar_last("t",inverso)
elif args.filtro == "c":
    filtrar_last("c",inverso)
elif args.filtro == "f":
    filtrar_last("f",inverso)
elif args.filtro == "n":
    filtrar_last("n",inverso)
elif args.filtro == "d":
    filtrar_last("d",inverso)
## Si la persona ingresa -r (recuento_horas) y -i (inverso), lo que se hace es guardar el resultado del bash en una lista
## y luego lo que hacemos es imprimir cada linea, de atrás para adelante, pero eliminando las ultimas 3 lineas 
## (espacio-sumatoria-espacio), y terminamos en el 1 para evitar los cabezales.
## Al finalizar, si la opción -i esta seleccionada, entonces hacemos un print de la lista[-2] que es la sumatoria de datos al final.
elif inverso and args.recuento_horas:
    lista,cabezales, suma_valores = normalizar_lista()
    print(cabezales)
    for i in range(len(lista)-3, 1, -1):
        print(lista[i])
    print("\n")
    print(suma_valores)
elif inverso:
    #lista, lista_normalizada, cabezales, suma_valores = normalizar_lista()
    lista = normalizar_lista()
    print(lista[0][0])
    for i in range(len(lista[0])-3, 1, -1):
        print(lista[0][i])
## Si no se ingresa ningún parametro, imprimimos tal cual el resultado de la salida estandar del bash.
else:
    print(output[0].decode(), file = sys.stderr, end="")
    print("\n")
exit()