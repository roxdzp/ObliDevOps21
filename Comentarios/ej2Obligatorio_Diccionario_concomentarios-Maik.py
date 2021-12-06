#!/opt/rh/rh-python36/root/usr/bin/python3.6  
## Esta linea indica el camino donde esta el python 3.6

# -*- coding: utf-8 -*-  
# ## Esta linea permite la utilización de un formato de codificación de caracteres Unicode. permite el uso de tildes sin errores.

#################################################################################################################################################
################################################# Comunicacion entre Python y Bash ##############################################################
#################################################################################################################################################

from os import PRIO_USER, pread
# Esta linea no la usamos en el script pero en lo que entregamos la pusimos, tenemos que saber que es.
# os — Interfaces misceláneas del sistema operativo
# Este módulo provee una manera versátil de usar funcionalidades dependientes del sistema operativo.
# os.pread: Lee como máximo n bytes del descriptor de archivo fd en una posición de offset, sin modificar el desplazamiento (offset) del archivo.
# os.PRIO_USER: Es para setearle parámetros para las funciones getpriority() y setpriority() que no usamos.


from subprocess import Popen, PIPE
# Se importa la función Popen del módulo subprocess de Python.
# Esta función permite ejecutar comandos de Linux en Python (permitirá ejecutar el script de la parte 1 del obligatorio).
# También se importa PIPE del módulo subprocess, para poder manejar
# la salida estándar y la salida estándar de errores del comando
# (del script del ejercicio 1).

import sys, argparse, re
# El módulo sys es útil para poder desplegar un mensaje en la salida estándar de errores.
# Se utiliza el módulo argparse para interpretar los parámetros recibidos por este script Python, argument parser (agarra los argumentos y los digiere).
# es un equivalente al getops mas pro.
# Segun el profe, parseo es cuando agarramos determinado flujo de caracteres o secuencoa de simbolos y hacer algun tipo de analisis/procesamiento/intepretacion de ese flujo.
# El re es utilizado para expresiones regulares, si queremos utilizar REGEX debemos importar re.
# El modulo argparse facilita al usuario la utilización de argumentos en la linea de comandos.
# El programa define que argumentos son necesarios (obligatorios), cuales no son obligatorios, y cuales NO son argumentos validos.
# Además el parse_args() nos permite generar automaticamente mensajes de ayuda sobre la utilización de los argumentos y controla los argumentos que sean
# invalidos.

"""
INFORMACIÓN COMPLEMENTARIA, SOLO A MODO DE EJEMPLO, USÁNDOSE EL MODULO
SYS PARA ACCEDER A LOS PARÁMETROS RECIBIDOS POR EL SCRIPT EN PYTHON.
# El módulo sys permite acceder a los parámetros recibidos por el script
# Python usando la variable sys.argv, que es una lista con los parámetros
# recibidos, pero como se usará el módulo argparse, estas líneas quedaran comentadas.
import sys
print ("Número de parámetros: ", len(sys.argv))
print ("Lista de argumentos: ", sys.argv)
"""

## Guardamos en variable la ruta del script de bash que usaremos para obtener los valores a trabajar
ej1_last = ['/root/ObliDevOps21/ej1Obligatorio.sh']

## Utilizamos argparse (que importamos previamente), para poder trabajar los parametros del script de Python.
## Me guardo en la variable parser la funcion argparse.ArgumentParser() 
## que es la funcion con la que voy a recibir los parametros del python y los voy mandar al bash.
parser = argparse.ArgumentParser()
# Basicamente en esta linea lo que estamos haciendo es contruir el parseador.
# Llamo al modulo argparse, con la funcion argumentparser y creamos el objeto parseador.

# Una vez importada la libreria argparse y contruido el parseador, no nos queda mas que empezar a trabajar
# con los argumentos. Para empezar a agregar argumentos usamos parser.add_argument(), un ejemplo seria parser.add_argument (prueba).

## El argumento -r viene del script de bash, lo utilizamos para validar si se devuelven o no la cantidad de minutos/horas/días. 
## Guarda en si, el valor true si se utiliza y en caso contrario false (esta o no esta).
## El nombre Largo ademas de que se estila poner, me sirve para evitar confuciones en el script, imaginemos querer borrar algo que solo sea -r.
parser.add_argument("-r", "--recuento_horas", help="Devuelve un contador de las horas/minutos/dias sumadas.", action="store_true")
## ¿Por que aca no le ponemos que sea de clase str como en las demas lineas?, para que le agregas la accion? y por que no se le pone un resultado por defecto como en las demas lineas?.
## Respuesta: No le ponemos str porque en -r no voy a guardar un string, solo me voy a guardar un booleano que va a ser un verdadero en caso de que el arguemtno sea r.
## No le pongo valor por default por que no lo necesito.

## El argumento -u es para introducir la variable del username a filtrar, se guarda en args.usuario y es de tipo string
parser.add_argument("-u", "--usuario", type=str, default=" ", help="Nos permite buscar las horas de un usuario en particular, va a compañado de una variable que es el nombre de usuario.")
## ¿Para que usas el default aca?, Respuesta, es para que la libreria argparse no me devuelva su error por defecto y poder poner el que yo le adjudique.

## El argumento -o nos permite ordenar por el valor introducido, u para usuario, t para terminal, h para host y d para 
## duración total de la conexión.
parser.add_argument("-o", "--orden", type=str, choices=["u", "t", "h", "d"], help="Ordenar de forma creciente la salida del LAST por una de las cuatro columnas a seleccionar.")

## El parametro -f nos permite filtrar la lista, quitando la columna filtrada, u para usuario, t para termina, h para host
## f para fecha, c para hora de conexion, n para hora de desconexion y d para duracion total de la conexion
parser.add_argument("-f", "--filtro", type=str, choices=["u", "t", "h", "f", "c", "n", "d"], help="Filtrado de listado (quita opciones).", nargs='+')

## El argumento -i nos permite definir si queremos invertir el orden de la lista recibida o no.
parser.add_argument("-i", "--inverso", help="Devuelve el listado de los valores ordenados con el -o pero de forma inversa.", action="store_true")

## Acá lo que hacemos es parsear los parametros recibidos de forma que se cargen en la variable args.
## Parsear es basicamente convertir estos parametros a un objeto-clase donde se guardan todos los parametros recibidos y luego pueden ser
## llamados de forma que el parametro inverso es args.inverso y el filtro es args.filtro. Esto es porque el objeto args contiene los atributos
## que son nuestros parametros.
## Si se recibe un error porque algun parametro este incorrecto y/o el orden no sea valido, se devuelve un mensaje y se manda un exit con 
# returncode 25
## try == intento (traducido). Lo que hace es intentar cargar la lista args de los argumentos introducidos por el usuario a la hora de ejecutar el script
## pero lo hace en base a las condiciones de nuestros argumentos, los cuales cargamos con la función add_argument() previamente.
## Resumiendo, se procesan los argumentos recibidos por el script en Python.
## Se captura la excepción SystemExit para poder salir con el código
## de salida que se pide en el ejercicio 2 y no con el código de salida que genere parser.parse_args().
try:
    args = parser.parse_args() # Esto me deja los parametros ya digeridos
    """
    El parse_args valida las acciones y tipo de datos introducidos en los parametros, lo que significa para nosotros, es que va a validar si nuestros parametros
    y sus datos correspondientes (en caso de ser solicitados, por ejemplo un string o un store_true), son correlativos a lo introducido por el usuarios.
    Además, en caso de que todos los argumentos introducidos sean validos, genera la lista de nuestros parametros recibidos y sus 
    tipos de datos (string, store_true, choices) correspondientes.
    """
    # En caso de que el usuario ingrese algo mal, dispara la exepcion SystemExit.
    # En la variable e se guarda todo el mensaje y una cnatidad de info de la exepcion va ahi.
except SystemExit as e:
    print("Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.")
    exit(25)

## Si la persona ingresa -r, entonces se le agrega a la lista del ej1_last, que es el script de bash, el parametro -r
## Este se carga primero por limitante de bash que nos obliga a ingresar -r como primero en caso de recibir -r y -u
if args.recuento_horas:
    ej1_last.append("-r")

## Si la persona ingresa -u, entonces se le agrega a la lista del ej1_last, que es el script de bash, el parametro -u con el valor del usuario cargado
if args.usuario:
    ej1_last.append("-u")
    ej1_last.append(args.usuario)

# Para obtener la salida estándar, la salida estándar de errores y el
# código de salida del script del ejercicio 1, se usa Popen, pasándole el
# comando con sus argumentos como una lista (cargada en la variable
# ej1_y_lista_parametros), donde el primer elemento es el comando y los
# siguientes son sus parámetros. Después de esa lista, a Popen se le
# pasa stdout = PIPE y stderr = PIPE para poder recuperar después la
# salida estándar y la salida estándar de errores.
## Creamos un proceso a traves de Popen y le pasamos la lista ej1_last, y las variables donde guardaremos la
## salida estandar y la salida de error.
process = Popen(ej1_last, stdout = PIPE, stderr = PIPE)
# aca estamos creando el ejecutador, esto lo hace popen, que es al que le paso la lista de lo que tiene que ejecutar, 
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
# El objeto process permite ejecutar el comando solicitado y acceder a la
# información que produce. Para obtener el código de retorno, la salida
# estándar y la salida estándar de errores del script del ejercicio 1, es
# necesario ejecutar el método communicate de este objeto (este método
# causa la ejecución del ejercicio 1).
# El método communicate retorna una tupla con la salida y la entrada
# estándar (stdoutdata, stderrdata). La variable output será una tupla
# con la salida estándar como primer elemento y la salida estándar de
# errores como segundo elemento.

## En ouput nos guardamos lo que nos devuelve nuestro script de bash, de forma que podemos imprimirlo en pantalla nuevamente.
output = process.communicate()
# Aca recien nos estamos comunicando como quien dice con el script de bash y en utput se carga la salida estandar y la salida estandar de errores.
# Aca se va a cargar una tupla con el codigo de salida 0 y la salida estandar y el codigo 1 y la salida estandar de errores.

# Con process.returncode se obtiene el código de retorno (exit code) del
# script del ejercicio 1.
# Si el código de retorno del script del ejercicio 1 es distinto de 0,
# entonces hay un error y por tanto hay que desplegar por la salida
# estándar de errores el mismo mensaje de error que ha devuelto ese
# script, además salir con su mismo código de error.

## Si nos devuelve error, osea que el codigo retornado por el script en bash es mayor a 0, entonces imprimimos
## en pantalla ese mensaje de error que viene de bash y nos salimos con exit y el mismo codigo del de bash.
## La función .decode() nos permite hacer que python utilize el mismo lenguaje de lectura que el de bash, que en este caso es UTF-8
## esto nos permite que se comporte de misma manera los saltos de lineas, espacios y tabulaciones y no veamos distorcionada la salida
## del script de bash en nuestra terminal de python.
if process.returncode > 0:
 # Se despliega el mensaje producido por el script del ejercicio 1 por
 # la salida estándar de errores.
 # Se usa el método decode para formatear correctamente la salida para
 # ser impresa. Podría usarse en este caso también .decode('utf-8').

    print(output[1].decode(), file = sys.stderr, end="")
    # output[1] es la salida de error, es el segundo elemento ya que empieza desde cero.
    # file = sys.stderr, es el equivalente a poner >&2 en bash.
    # end="" es para que no me agregue un enter mas, la propia salida de la salida estandar de errores ya tiene un enter, si le sumo el enter del print
    # me van a quedar dos, por eso es que le digo que al final no le meta nada.
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
#esa linea es la exepcion, es la parte que la letra pide que saquemos un caso de exito por la salida estandar de errores.
# la diferencia entre el primer if con el segundo, es que en el primero atajo un error y en el segundo un warning.

#################################################################################################################################################
############################################################# FUNCIONES #########################################################################
#################################################################################################################################################

##########
##########

## LA FUNCION LISTANORMALIZADA (normalizar_lista) NO ES NECESARIA AHORA QUE DESDE EL DE BASH SE FILTRAN LAS LINEAS DEL USUARIO REBOOT SYSTEM BOOT.
## POR LO QUE TODA ESTA FUNCION SE PUEDE ELIMINAR; DADO QUE LO UNICO QUE HACE ES NORMALIZAR UNA LISTA YA NORMALIZADA.
## PERO COMO NO NOS DIMOS CUENTA, QUEDO CREADA Y POR ENDE HAY QUE ENTENDER COMO FUNCIONA.
## SI NOSOTROS LA BORRAMOS NO AFECTA EN NADA AL PROGRAMA.

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
    ## Con el for i in range(0,10): lo que yo hago es repetir mi for del 0 al 10 y el valor de la variable i va cambiando en cada iteración, de forma que toma
    ## cada valor en el range() solicitado.
    ## Empiezo en la posición 1 porque los cabezales que se encuentran en la posición 0 los quiero evitar.
    for i in range(1,rango): ## Por cada valor en el rango (rango es la longitud total de la lista que retorna el script de bash).
        if lista[i].split(" ")[0] != "" : ## Si la linea es vacia, no hago nada, en caso contrario la normalizo.
    # Si la lista en esa posicion, separada por espacios y quedandome con la pocicion 0 es diferente de vacia, then...
            linea=re.sub(' +', ' ', lista[i]) ## A mi linea le reemplazo todos los espacios multiples y le pongo un solo espacio (esto es para poder splitear).
            # lines va a ser la sustitucion de espacios indefinidos por uno solo.
            fila="" ## inicializo como vacia la fila que se va ir rellenando con los valores normalizados, osea "usuario  " "term         ", etc...
            for longitud in range(0,len(lista_longitudes)): ## Por cada longitud (nombre de mi variable, podia ser i, j, x, pepe o carlitos)
                                                            ## lo que hago es recorrer todos los valores de mi lista_longitudes
                                                            ## de forma que voy uno a uno del 9 al 7, para poder validar si el valor de la columna usuario
                                                            ## es igual, menor o mayor a esa longitud.
                if len(linea.split(" ")[longitud]) <= lista_longitudes[longitud]: ## Si el valor  de nuestra columna (usuario, term, host, etc..) es menor
                                                                                ## a nuestro valor de la lista de longitudes (9,13,17,4... etc).
                                                                                ## Entonces debo de "rellenar" con espacios los valores de esa columna
                                                                                ## Y luego la guardo en nuestra variable fila inicializada previamente.
                    fila=fila+linea.split(" ")[longitud].ljust(lista_longitudes[longitud]) ## ljust agrega espacios a la derecha (left) de una cadena de
                                                                                            ## caracteres HASTA la cantidad asignada en la función.
                else: ## Si nuestro valor de la columna (usuario, term, host, etc...) es mayor a 9, es porque debo recortar esa lina antes de cargarla en
                        ## nuestra fila, para hacer eso utilizo [:hasta la longitud deseada]. Y este valor es cargado en nuestra fila.
                    fila=fila+linea.split(" ")[:lista_longitudes[longitud]] ## Si me pasa que la linea es más larga de lo que yo necesito, la corto, usando
                                                                            ## [:hastalalongituddeseada].
            lista_normalizada.append(fila) ## Al finalizar el for que recorre cada columna de neustra linea, genero una fila con los valores normalizados
                                            ## es decir que nuestra fila tiene cada columna con su longitud (valor+espacios) correspondiente
                                            ## Lo que para nosotros sería una "fila valida", por lo que podemos guardarla en nuestra lista_normalizada.
    return lista_normalizada, suma_valores

    ############
    ############

## Creamos una función que nos convierte nuestra lista en una lista de diccionarios, donde las claves de ese 
## diccionario sean los cabezales de nuestro LAST (Usuario, Term, Host...).
## lista=[{"Usuario":"root","Term":"tty2"...},{},{},{}]
## lista.sort(key = lambda ele:ele["Usuario"])

def lista_diccionario(lista):
    diccionario={} ## Inicializo el diccionario
    lista_diccionario=[] ## Inicializo la lista de diccionarios
    ## Por cada linea de nuestra lista creamos un diccionario con los datos correspondientes a cargar.
    ## Se observa que el diccionario se carga por el valor de la longitud de cada columna, de modo que la primera
    ## que es la del usuario va del 0 al 9 y la segunda va del 9 + 13 (longitud de la columna Term), osea que va
    ## del 9 al 22 y así sucesivamente.
    for linea in lista: ## Por cada linea de mis lista de listas (osea por cada lista de mi lista de listas).
        diccionario={"Usuario":linea[:9],"Term":linea[9:22],"Host":linea[22:39],"Fecha":linea[39:43]+linea[43:47]+linea[47:50],"H.Con":linea[50:56],"-":linea[56:58],"H.Des":linea[58:65],"T.Con":linea[65:72]}
        lista_diccionario.append(diccionario) ## Una vez que creo el diccionario, lo cargo en mi lista de diccionarios, de forma que al final obtengo
                                             ## una lista de diccionarios.
    return lista_diccionario

#########################################################################################################################################################################
############################################################# EL SCRIPT #################################################################################################
#########################################################################################################################################################################
## Cargamos una lista desde el return de nuestra función lista normalizada.
## Dado que nos devuelve 2 valores, la lista en la posicion [0] y la suma de valores (en caso de ingresar -r)
## en la posición [1].
lista=normalizar_lista()

## Pasamos esa lista a la función lista_diccionario y nos devuelve la lista de diccionarios.
lista=lista_diccionario(lista[0])

## Si se ingresa el atributo -u con alguno de sus valores del choise, entonces ordena por ese valor nuestra lista.
if args.orden == "u":
    lista.sort(key = lambda ele:ele["Usuario"]) ## este Lambda recorre todos los diccionarios de mi lista de diccionarios y luego ordena en base a la clave que
                                                ## yo le paso como parametro, en este caso por usuario.
                                                ## El resultado es una lista de diccionarios que esta ordenada por la clave Usuario (de menor a mayor).
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
if args.filtro != None: ## Si no se ingresa el -f, entonces no hago nada. En caso contrario, empiezo a filtrar.
    if len(args.filtro) >= 7:
        print("Al menos un campo debe estar visible, no pudiéndose ocultar todos.")
        exit(20)
    ## Dado que este atributo es de tipo nargs='+', entonces debemos buscar todas las columnas a filtrar (borrar)-
    for i in args.filtro:
        ## Por cada valor ingresado, se popea (elimina) la columna que tenga como Key el valor ingresado a filtrar.
        if i == "u":
            cabezales.remove("Usuario  ") ## Remuerve de mi lista de cabezales el cabezal Usuario, para que al imprimir los cabezales, no aparezca el filtrado.
            for diccionario in lista:
                diccionario.pop("Usuario") ## Por cada diccionario en mi lista de diccionarios, elimino (popeo) la clave Usuario con su elemento correspondiente
                                            ## esto se repite para todos los diccionarios de mi lista y para cada caso de filtrado -f u d t... etc
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
linea="" ## creando la linea
for cabezal in cabezales: ## Por cada cabezal en mi lista de cabezales que ahora esta filtrada. Lo que debo hacer es crear una nueva linea (mis cabezales)
                            ## he imprimirlos en pantalla.
    linea=linea+cabezal
print(linea)

## Si args.inverso es verdadero, entonces el inverso es -1 de forma que al listar los elementos se listan con paso
## -1, en caso de que args.inverso sea falso, el inverso vale 1 y por ende el paso es 1.
inverso=1
if args.inverso:
    inverso=-1

## La variable claves se guarda en si misma el valor de todas las claves de uno de nuestros diccionarios de mi lista de
## diccionarios, en este caso el de la posición 0. Esto es así porque todos nuestros diccionarios tienen las mismas
## claves.
claves=lista[0].claves()
for elemento in lista[::inverso]:
    linea=""
    for clave in claves:
        linea=linea+elemento[clave]
    print(linea)

## Si se ingreso -r, entonces se imprime la linea del -r (suma de las horas/minutos/días)
## Además luego se valida si se ingreso o no un usuario para el -u de forma que podamos imprimir la cantidad de
## de lineas, personalizando el mensaje por el usuario al cual se le imprimen esas lineas.

#Aca muestro la lista dependiendo de si se ingreso el parametro -r o no, si no lo ingrese te mando el last como viene.
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


    