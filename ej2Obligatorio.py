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

## Acá lo que hacemos es parsear los parametros recibidos de forma que se cargen en la variable args.
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

## Creamos un proceso a traves de Popen y le pasamos la lista ej1_last, y las variables donde guardaremos la
## salida estandar y la salida de error.
process = Popen(ej1_last, stdout = PIPE, stderr = PIPE)

output = process.communicate()

## Si nos devuelve error, osea que el codigo retornado por el script en bash es mayor a 0, entonces imprimimos
## en pantalla ese mensaje de error que viene de bash y nos salimos con exit y el mismo codigo del de bash.
if process.returncode > 0:
    print(output[1].decode(), file = sys.stderr, end="")
    exit(process.returncode)

if output[1].decode() != "":
    print(output[1].decode(), file=sys.stderr, end="")
    exit(0)

## Si no se ingresa ningun parametro, se hace bypass de la salida standar de bash en nuestro script de python.
## Pero se le agrega la cuenta de conexiones.
if args.recuento_horas == False and args.orden == None and args.filtro == None and args.inverso == False:
    print(output[0].decode(), file=sys.stderr, end="")
    print("\nCantidad de conexiones listadas:",len(output[0].decode().split("\n"))-2)
    exit(0)

## Si el unico atributo que se ingresa es -r imprimimos en pantalla la salida standar del de bash.
## Lo que sería basicamente bypass la salida standar del de bash por la de python.
if args.recuento_horas and args.orden == None and args.filtro == None and args.inverso == False:
    print(output[0].decode(), file=sys.stderr, end="")
    if args.usuario:
        print("\nCantidad de conexiones listadas para el usuario",args.usuario+":",len(output[0].decode().split("\n"))-3)
    else:
        print("\nCantidad de conexiones listadas:",len(output[0].decode().split("\n"))-2)
    exit(0)

## Creamos una función que nos normaliza una lista creada a partir de la salida standar del script de bash.
def normalizar_lista():
    ## Creamos una lista que esta creada creada en base a la salida estandar del script de bash, pero separado por
    ## los saltos de linea, lo que nos genera un dato en la lista por cada linea.
    lista=output[0].decode().split("\n")
    lista_normalizada=[]
    ## Si se ingresa -r, entonces obtenemos la linea -2 que es la que tiene los valores sumados.
    if args.recuento_horas :
        ## Ahora se carga cada valor de nuestra lista recibida por la salida estandar del bash, en una nueva lista donde cada valor esta
        ## separado por un unico espacio. Ya que estabamos en esto, si el usuario es reboot lo eliminamos de la lista.
        suma_valores=lista[-2]
        ## Para normalizar pasamos por cada linea y decimos que si el usuario es reboot o si la linea es vacia
        ## entonces no se carga en la lista.
        for i in range(1,len(lista)-2):
            if lista[i].split(" ")[0] != "" and lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores
    ## Si no se ingresa -r, entonces la variable de la suma de valores la inicializamos en vacio.
    else:
        suma_valores=""
        for i in range(1,len(lista)):
            if lista[i].split(" ")[0] != "" and lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores

## Creamos una función que nos convierte nuestra lista en una lista de diccionarios, donde las keys de ese 
## diccionario sean los cabezales de nuestro LAST (Usuario, Term, Host...).
def lista_diccionario(lista):
    diccionario={}
    lista_diccionario=[]
    ## Por cada linea de nuestra lista creamos un diccionario con los datos correspondientes a cargar.
    for linea in lista:
        diccionario={"Usuario":linea.split(" ")[0],"Term":linea.split(" ")[1],"Host":linea.split(" ")[2],"Fecha":linea.split(" ")[3]+" "+linea.split(" ")[4]+" "+linea.split(" ")[5],"H.Con":linea.split(" ")[6],"-":linea.split(" ")[7],"H.Des":linea.split(" ")[8],"T.Con":linea.split(" ")[9]}
        lista_diccionario.append(diccionario)
    return lista_diccionario

## Cargamos una lista desde el return de nuestra función lista normalizada.
## Dado que nos devuelve 2 valores, la lista en la posicion [0] y la suma de valores (en caso de ingresar -r)
## en la posición [1].
lista=normalizar_lista()

## Pasamos esa lista a la función lista_diccionario y nos devuelve la lista de diccionarios.
lista=lista_diccionario(lista[0])

## Si la persona ingresa -i entonces se carga una variable booleana llamada inverso, con True, en caso contrario
## se queda en False. Esto lo utilizamos en la lambda para decidir si el reverse=True o reverse=False. 
inverso=False
if args.inverso:
    inverso=True

## Si se ingresa el atributo -u con alguno de sus valores del choise, entonces ordena por ese valor nuestra lista.
if args.orden == "u":
    lista.sort(key = lambda ele:ele["Usuario"], reverse=inverso)
elif args.orden == "t":
    lista.sort(key = lambda ele:ele["Term"], reverse=inverso)
elif args.orden == "h":
    lista.sort(key = lambda ele:ele["Host"], reverse=inverso)
elif args.orden == "d":
    lista.sort(key = lambda ele:ele["T.Con"], reverse=inverso)

## Si no se ingresa el atributo -f con alguno de sus valores, entonces se sigue de largo
## En caso de que si se ingresen, primero validamos que no se hayan ingresado todos
## De ser así, devolvemos el mensaje de error "Al menos un campo debe estar visible, no pudiéndose ocultar todos"
if args.filtro != None:
    lista_filtros=['u', 'd', 'f', 'h', 't', 'n', 'c']
    if(set(args.filtro) == set(lista_filtros)):
        print("Al menos un campo debe estar visible, no pudiéndose ocultar todos")
        exit(20)
    ## Dado que este atributo es de tipo nargs='+', entonces debemos buscar todas las columnas a filtrar (borrar)-
    for i in args.filtro:
        ## Por cada valor ingresado, se popea (elimina) la columna que tenga como Key el valor ingresado a filtrar.
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

## Obtenemos una lista de todas las keys de uno de nuestro diccionarios, el de la posición [0].
## Para obtener esos valores usamos la función .keys
cabezales=lista[0].keys()
linea=""
## Una vez que tenemos estas keys, las vamos a utilizar como cabezales, de forma que luego podamos imprimir los 
## necesarios para cada caso filtrado. Y luego unicamente vamos dandole "formato" a estos cabezales en pantalla
for cabezal in cabezales:
    if cabezal == "Fecha" or cabezal == "Host":
        linea=linea+cabezal+"\t"+"\t"
    else:
        linea=linea+cabezal+"\t"
print(linea)
## Se imprime nuestra lista en pantalla con los valores ya filtrados y ordenados
for elemento in lista:
    linea=""
    for key in cabezales:
        if key == "Host" and elemento[key] == "tty2":
            linea=linea+elemento[key]+"\t"+"\t"
        else:
            linea=linea+elemento[key]+"\t"
    print(linea)

## Si se ingreso -r, entonces se imprime la linea del -r (suma de las horas/minutos/días)
if args.recuento_horas:
    suma_valores=normalizar_lista()
    print("\n")
    print(suma_valores[1])
    if args.usuario:
        print("\nCantidad de conexiones listadas para el usuario",args.usuario+":",len(output[0].decode().split("\n"))-3)
    else:
        print("\nCantidad de conexiones listadas:",len(output[0].decode().split("\n"))-2)
    
    exit(0)
