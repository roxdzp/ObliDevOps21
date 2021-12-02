#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
from os import PRIO_USER, pread
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

## Creamos una función que nos normaliza una lista creada a partir de la salida standar del script de bash.
def normalizar_lista():
    ## Creamos una lista que esta creada en base a la salida estandar del script de bash, pero separado por
    ## los saltos de linea, lo que nos genera un dato en la lista por cada linea.
    lista=output[0].decode().split("\n")
    lista_normalizada=[]
    ## Esta lista de longitudes nos permite definir el tamaño de cada columna en cantidad de caracteres.
    ## Si una columna no llega a tener este temaño, se debe rellenar con espacios con ljust().
    lista_longitudes=[9,13,17,4,4,3,6,2,7,7]
    ## Si se ingresa -r, entonces obtenemos la linea -2 que es la que tiene los valores sumados.
    if args.recuento_horas :
        ## Ahora se carga cada valor de nuestra lista recibida por la salida estandar del bash, en una nueva lista donde cada valor esta
        ## separado por un unico espacio. Ya que estabamos en esto, si el usuario es reboot lo eliminamos de la lista.
        suma_valores=lista[-2]
        ## La variable rango nos permite determinar hasta donde se va a ejecutar el for que itera por cada linea
        ## de nuestra lista que es la salida standar de bash. Utilizamos -2 cuando se ingresa -r para saltear la
        ## linea que nos da el contador de dias/horas/minutos y la linea en blanco.
        rango=len(lista)-2
        ## Para normalizar pasamos por cada linea y decimos que si el usuario es reboot o si la linea es vacia
        ## entonces no se carga en la lista.
    ## Si no se ingresa -r, entonces la variable de la suma de valores la inicializamos en vacio.
    else:
        suma_valores=""
        rango=len(lista)
    ## Se crea un for que nos permite pasar por cada linea de nuestra lista (una linea del last distinta)
    ## y una vez hecho esto, si la linea es distinta de vacio, entonces se le procesa de forma que cada columna
    ## de esa linea, tenga la longitud asignada en la lista de longitudes. De este modo la columna del Usuario
    ## obtiene una cantidad de 9 caracteres (El usuario+espacios) sin importar el nombre del usuario.
    ## Este mismo proceso se corre para cada columna (Usuario, Term, Host, Fecha, etc...)
    for i in range(1,rango):
        if lista[i].split(" ")[0] != "" :
            linea=re.sub(' +', ' ', lista[i])
            fila=""
            for longitud in range(0,len(lista_longitudes)):
                if len(linea.split(" ")[longitud]) <= lista_longitudes[longitud]:
                    fila=fila+linea.split(" ")[longitud].ljust(lista_longitudes[longitud])
                else:
                    fila=fila+linea.split(" ")[0:lista_longitudes[longitud]]
            lista_normalizada.append(fila)
    return lista_normalizada, suma_valores

## Creamos una función que nos convierte nuestra lista en una lista de diccionarios, donde las keys de ese 
## diccionario sean los cabezales de nuestro LAST (Usuario, Term, Host...).
def lista_diccionario(lista):
    diccionario={}
    lista_diccionario=[]
    ## Por cada linea de nuestra lista creamos un diccionario con los datos correspondientes a cargar.
    ## Se observa que el diccionario se carga por el valor de la longitud de cada columna, de modo que la primera
    ## que es la del usuario va del 0 al 9 y la segunda va del 9 + 13 (longitud de la columna Term), osea que va
    ## del 9 al 22 y así sucesivamente.
    for linea in lista:
        diccionario={"Usuario":linea[:9],"Term":linea[9:22],"Host":linea[22:39],"Fecha":linea[39:43]+linea[43:47]+linea[47:50],"H.Con":linea[50:56],"-":linea[56:58],"H.Des":linea[58:65],"T.Con":linea[65:72]}
        lista_diccionario.append(diccionario)
    return lista_diccionario

## Cargamos una lista desde el return de nuestra función lista normalizada.
## Dado que nos devuelve 2 valores, la lista en la posicion [0] y la suma de valores (en caso de ingresar -r)
## en la posición [1].
lista=normalizar_lista()

## Pasamos esa lista a la función lista_diccionario y nos devuelve la lista de diccionarios.
lista=lista_diccionario(lista[0])

## Si se ingresa el atributo -u con alguno de sus valores del choise, entonces ordena por ese valor nuestra lista.
if args.orden == "u":
    lista.sort(key = lambda ele:ele["Usuario"])
elif args.orden == "t":
    lista.sort(key = lambda ele:ele["Term"])
elif args.orden == "h":
    lista.sort(key = lambda ele:ele["Host"])
elif args.orden == "d":
    lista.sort(key = lambda ele:ele["T.Con"])

## Creo una lista con los cabezales que se van a imprimir, de modo que luego puedo ir borrando sus valores
## en caso de que el usuario ingrese parametros para filtrar nuestra lista. De esta forma si se elimina la columna
## del usuario, además de borrar de mi lista de diccionarios, todos los valores de la key Usuario, también
## borro el valor de mi lista de cabezales que coincida con Usuario.
cabezales=["Usuario  ","Term         ","Host             ","Fecha      ","H.Con ","- ","H.Des  ","T.Con  "]
## Si no se ingresa el atributo -f con alguno de sus valores, entonces se sigue de largo
## En caso de que si se ingresen, primero validamos que no se hayan ingresado todos
## De ser así, devolvemos el mensaje de error "Al menos un campo debe estar visible, no pudiéndose ocultar todos"
if args.filtro != None:
    if len(args.filtro) >= 7:
        print("Al menos un campo debe estar visible, no pudiéndose ocultar todos.")
        exit(20)
    ## Dado que este atributo es de tipo nargs='+', entonces debemos buscar todas las columnas a filtrar (borrar)-
    for i in args.filtro:
        ## Por cada valor ingresado, se popea (elimina) la columna que tenga como Key el valor ingresado a filtrar.
        if i == "u":
            cabezales.remove("Usuario  ")
            for diccionario in lista:
                diccionario.pop("Usuario")
        elif i == "t":
            cabezales.remove("Term         ")
            for diccionario in lista:
                diccionario.pop("Term")
        elif i == "h":
            cabezales.remove("Host             ")
            for diccionario in lista:
                diccionario.pop("Host")
        elif i == "f":
            cabezales.remove("Fecha      ")
            for diccionario in lista:
                diccionario.pop("Fecha")
        elif i == "c":
            cabezales.remove("H.Con ")
            cabezales.remove("- ")
            for diccionario in lista:
                diccionario.pop("H.Con")
            for diccionario in lista:
                diccionario.pop("-")
        elif i == "n":
            cabezales.remove("H.Des  ")
            for diccionario in lista:
                diccionario.pop("H.Des")
        elif i == "d":
            cabezales.remove("T.Con  ")
            for diccionario in lista:
                diccionario.pop("T.Con")

## Acá se crea una linea con todos los cabezales y luego se imprime en pantalla.
linea=""
for cabezal in cabezales:
    linea=linea+cabezal
print(linea)

## Si args.inverso es verdadero, entonces el inverso es -1 de forma que al listar los elementos se listan con paso
## -1, en caso de que args.inverso sea falso, el inverso vale 1 y por ende el paso es 1.
inverso=1
if args.inverso:
    inverso=-1

## La variable keys se guarda en si misma el valor de todas las keys de uno de nuestros diccionarios de mi lista de
## diccionarios, en este caso el de la posición 0. Esto es así porque todos nuestros diccionarios tienen las mismas
## keys.
keys=lista[0].keys()
for elemento in lista[::inverso]:
    linea=""
    for key in keys:
        linea=linea+elemento[key]
    print(linea)

## Si se ingreso -r, entonces se imprime la linea del -r (suma de las horas/minutos/días)
## Además luego se valida si se ingreso o no un usuario para el -u de forma que podamos imprimir la cantidad de
## de lineas, personalizando el mensaje por el usuario al cual se le imprimen esas lineas.
if normalizar_lista()[1] != "":
    print("\n")
    print(normalizar_lista()[1])
    if args.usuario:
        print("\nCantidad de conexiones listadas para el usuario",args.usuario+":",len(output[0].decode().split("\n"))-4)
    else:
        print("\nCantidad de conexiones listadas:",len(output[0].decode().split("\n"))-2)
    exit(0)
else:
    if args.usuario:
        print("\nCantidad de conexiones listadas para el usuario",args.usuario+":",len(output[0].decode().split("\n"))-2)
    else:
        print("\nCantidad de conexiones listadas:",len(output[0].decode().split("\n"))-2)
    exit(0)