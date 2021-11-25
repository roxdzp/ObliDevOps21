#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
from os import pread
from subprocess import Popen, PIPE

import sys, argparse, re

## Guardamos en variable la ruta del script de bash que usaremos para obtener los valores a trabajar

ej1_last = ['/root/ObliDevOps21/ej1Obligatorio.sh']

## Utilizamos argparse (que importamos previamente), para poder trabajar los parametros del script de Python.

parser = argparse.ArgumentParser()

## El argumento -r viene del script de bash, lo utilizamos para validar si se devuelven o no la cantidad de minutos/horas/días. 
## Guarda en si el valor true si se utiliza y en caso contrario false.

parser.add_argument("-r", "--recuento_horas", help="Devuelve un contador de las horas/minutos/dias sumadas.", action="store_true")

## El argumento -u es para introducir la variable del username a filtrar, se guarda en args.usuario y es de tipo string

parser.add_argument("-u", "--usuario", type=str, default="", help="Nos permite buscar las horas de un usuario en particular, va a compañado de una variable que es el nombre de usuario.")

## El argumento -o nos permite ordenar por el valor introducido, u para usuario, t para termina, h para host y d para 
## duración total de la conexión.

parser.add_argument("-o", "--orden", type=str, choices=["u", "t", "h", "d"], help="Ordenar de forma creciente la salida del LAST por una de las cuatro columnas a seleccionar.")

## El parametro -f nos permite filtrar la lista, quitando la columna filtrada, u para usuario, t para termina, h para host
## f para fecha, c para hora de conexion, n para hora de desconexion y d para duracion total de la conexion
parser.add_argument("-f", "--filtro", type=str, choices=["u", "t", "h", "f", "c", "n", "d"], help="Filtrado de listado (quita opciones).", nargs='+')

## El argumento -i nos permite definir si queremos invertir el orden de la lista recibida o no.
parser.add_argument("-i", "--inverso", help="Devuelve el listado de los valores ordenados con el -o pero de forma inversa.", action="store_true")

## Acá lo que haceoms es parsear los parametros recibidos de forma que se cargen en la variable args.
try:
    args = parser.parse_args()
except SystemExit as e:
    print("Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.")
    exit(25)

## Si la persona ingresa -r, entonces se le agrega a la lista del ej1_last, que es el script de bash, el parametro -r
if args.recuento_horas:
    ej1_last.append("-r")

## Si la persona ingresa -u, entonces se le agrega a la lista del ej1_last, que es el script de bash, el parametro -u con el valor del usuario cargado
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

lista=output[0].decode().split("\n")

def normalizar_lista():
    lista=output[0].decode().split("\n")
    lista_normalizada=[]
    if args.recuento_horas :
        ## Si se ingresa -r, entonces obtenemos la linea -2 que es la que tiene los valores sumados.
        suma_valores=lista[-2]
        ## Ahora se carga cada valor de nuestra lista recibida por la salida estandar del bash, en una nueva lista donde cada valor esta
        ## separado por un unico espacio. Ya que estabamos en esto, si el usuario es reboot lo eliminamos de la lista.
        for i in range(1,len(lista)-3):
            if lista[i].split(" ")[0] != "reboot" and lista[i].split(" ")[0] != "" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores
    else:
        ## Si no se ingresa -r, entonces la variable de la suma de valores la inicializamos en vacio.
        suma_valores=""
        for i in range(1,len(lista)):
            if lista[i].split(" ")[0] != "reboot" and lista[i].split(" ")[0] != "" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores

def lista_diccionario(lista):
    usuario=[]
    term=[]
    host=[]
    fecha=[]
    hcon=[]
    separador=[]
    hdes=[]
    tcon=[]
    for linea in lista:
        usuario.append(linea.split(" ")[0])
        term.append(linea.split(" ")[1])
        host.append(linea.split(" ")[2])
        fecha.append(linea.split(" ")[3]+" "+linea.split(" ")[4]+" "+linea.split(" ")[5])
        hcon.append(linea.split(" ")[6])
        separador.append(linea.split(" ")[7])
        hdes.append(linea.split(" ")[8])
        tcon.append(linea.split(" ")[9])
    diccionario={}
    lista_diccionario=[]
    for i in range(0,len(usuario)):
        diccionario={"Usuario":usuario[i],"Term":term[i],"Host":host[i],"Fecha":fecha[i],"H.Con":hcon[i],"-":separador[i],"H.Des":hdes[i],"T.Con":tcon[i]}
        lista_diccionario.append(diccionario)
    return lista_diccionario

lista=normalizar_lista()

lista=lista_diccionario(lista[0])

inverso=False
if args.inverso:
    inverso=True

if args.recuento_horas and args.orden == None and args.filtro == None and args.inverso == False:
    print(output[0].decode(), file=sys.stderr, end="")
    exit(0)

if args.orden == "u":
    lista.sort(key = lambda ele:ele["Usuario"], reverse=inverso)
elif args.orden == "t":
    lista.sort(key = lambda ele:ele["Term"], reverse=inverso)
elif args.orden == "h":
    lista.sort(key = lambda ele:ele["Host"], reverse=inverso)
elif args.orden == "d":
    lista.sort(key = lambda ele:ele["T.Con"], reverse=inverso)

if args.filtro != None:
    for i in args.filtro:
        if i == "u":
            for diccionario in lista:
                diccionario.pop("Usuario")
        elif i == "t":
            for diccionario in lista:
                diccionario.pop("Term")
        elif i == "h":
            for diccionario in lista:
                diccionario.pop("Host")
        elif i == "f":
            for diccionario in lista:
                diccionario.pop("Fecha")
        elif i == "c":
            for diccionario in lista:
                diccionario.pop("H.Con")
        elif i == "n":
            for diccionario in lista:
                diccionario.pop("H.Des")
        elif i == "d":
            for diccionario in lista:
                diccionario.pop("T.Con")
cabezales=lista[0].keys()
linea=""
for cabezal in cabezales:
    if cabezal == "Fecha" or cabezal == "Host":
        linea=linea+cabezal+"\t"+"\t"
    else:
        linea=linea+cabezal+"\t"
print(linea)
for elemento in lista:
    linea=""
    for key in cabezales:
        if key == "Host" and elemento[key] == "tty2":
            linea=linea+elemento[key]+"\t"+"\t"
        else:
            linea=linea+elemento[key]+"\t"
    print(linea)

if args.recuento_horas:
    suma_valores=normalizar_lista()
    print("\n")
    print(suma_valores[1])
    exit(0)
else:
    suma_valores=normalizar_lista()
    exit(0)