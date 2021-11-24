
#!/opt/rh/rh-python36/root/usr/bin/python3.6
# -*- coding: utf-8 -*-
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

## Normalizar lista es para poder obtener los valores recibidos de la salida estandar del bash y normalizarlos para trabajar con ellos.
## Esto nos permite filtrar, 
def normalizar_lista():
    ## Guardamos en una lista todas las lineas de la salida estandar del script de bash
    lista=output[0].decode().split("\n")
    ## Se carga una variable con los cabezales que va a tener nuestra lista.
    headers='Usuario Term Host Fecha - - H.Con - H.Des T.Con'
    ## La lista normalizada se inicializa y se le carga los headers.
    lista_normalizada=[]
    lista_normalizada.append(headers)
    if args.recuento_horas :
        ## Si se ingresa -r, entonces obtenemos la linea -2 que es la que tiene los valores sumados.
        suma_valores=lista[-2]
        ## Ahora se carga cada valor de nuestra lista recibida por la salida estandar del bash, en una nueva lista donde cada valor esta
        ## separado por un unico espacio. Ya que estabamos en esto, si el usuario es reboot lo eliminamos de la lista.
        for i in range(1,len(lista)-3):
            if lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores
    else:
        ## Si no se ingresa -r, entonces la variable de la suma de valores la inicializamos en vacio.
        suma_valores=""
        for i in range(1,len(lista)):
            if lista[i].split(" ")[0] != "reboot" :
                lista_normalizada.append(re.sub(' +', ' ', lista[i]))
        return lista_normalizada, suma_valores

## Creamos una función que nos permita filtrar por una columna en particular del LAST recibido.
def filtrar_last(opcion, lista_filtrada):
    ## Generamos un indice, el cual vamos a buscar en la lista_filtrada para determinar que indice de la lista debemos borrar, 
    ## en relación con la lista ya filtrada.
    indice=0
    if opcion == "u" :
        ## Acá buscamos el indice macheando por los cabezales lista_filtrada[0][i]
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Usuario':
                indice=i
        ## Borramos todas las filas encontradas en la lista_filtrada que macheen con el indice a borrar.
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    if opcion == "t" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Term':
                print("indice",indice)
                indice=i
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    elif opcion == "h" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Host':
                indice=i
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    elif opcion == "f" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'Fecha':
                indice=i
        ## Acá se repite 3 veces el borrado porque al normalizar, la fecha toma 3 columnas, día, mes, dia en numero.
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    elif opcion == "c" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'H.Con':
                indice=i
        ## Acá se repite 2 veces porque al normalizar, se pone un "-" como columna, que trabaja como separador de la hora de conexion y la
        ## hora de desconexion, entonces eliminamos la hora de conexión y el separador.
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    elif opcion == "n" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'H.Des':
                indice=i
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada
    elif opcion == "d" :
        for i in range(0,len(lista_filtrada[0])):
            if lista_filtrada[0][i] == 'T.Con':
                indice=i
        for fila in range(0,len(lista_filtrada)-1):
            lista_filtrada[fila].pop(indice)
        return lista_filtrada

## Creamos la lista filtrada como global porque vamos a trabajar esta lista en varios espacios del programa
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

## Entendemos que el proceso de trabajo de los datos es obtener la lista, luego ordenarla, filtrarla y por ultimo invertirla.
## En base a esa idea es como disponemos el como se obtienen los parametros.

## Al llegar acá entendemos que ya esta normalizada y ordenada nuestra lista (En caso de pedirse) por lo que solo imprimimos la lista.
if args.orden:
    lista_normalizada=lista_normalizada[0]    
    for j in range(0,len(lista_normalizada)):
        print(lista_normalizada[j])
    print("\n")
    exit(0)
## Con nuestra lista normalizada - filtrada - ordenada, si la persona ingresa -r se le agrega la suma de horas y al ser inverso = False
## no se invierte la lista.
elif args.recuento_horas and inverso == False :
    lista=normalizar_lista()
    for j in range(0,len(lista_normalizada)):
        print(lista_normalizada[j])
    print("\n")
    print(lista[1])
    exit(0)
## Si es -r y además tener inverso en True, entonces se invierte la lista y se agrega la suma de horas.
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
## Para todo el resto de los casos que no se ingresa nada, se devuelve el valor tal cual llega del bash
else: 
    print(output[0].decode(), file=sys.stderr, end="")
    exit(0)