#!/bin/bash

#########################################################################################################################################################################
############################################################# FUNCIONES #################################################################################################
#########################################################################################################################################################################
# Hay tres funciones:
# 1) "validaruser" La primera que valida que el usuario existe y trae las filas del last que le corresponden
# 2) "gethoursminutes" Procesa los tiempos de conexión y se los pasa a "converttime"
# 3) "converttime" Formatea los tiempos de conexión.

## Funcion que valida que un usuario exista
function validaruser
{
    ## Utilizamos -q para que grep no escriba en pantalla y utilizamos la regex=^$1: que nos busca el parametro 
    ## recibido de la funcion en el archivo
    ## solo si empieza con ese parametro $1 y esta acompañado de un : al final.

	if ! grep -q "^$1:" /etc/passwd # si el usuario que ingrese la persona no existe
	then
		return 1 # entonces retorna uno
	fi
}

## Esta funcion nos permite pasando dos parametros (hh y mm) convertir esas cantidades a dias, horas y minutos
## o a horas y minutos si los dias = 0 (minutos < 1440)
## Se debe de entender que 1440 minutos son 1 día y que 60 minutos son 1 hora.
function converttime # funcion para convertir las horas y minutos desde la salida del /etc/passwd
{ 	# La notación (( después de la llave es lo mismo que hacer "minutes=$($2*60)" >> Esta es la que dió el profe en clase, pero nacho es crack vió
    
    # Primero trabajamos con la cantidad de minutos totales
    ((minutes=$2*60)) # $2 son las horas, las multiplico por 60 para llegar a las horas
	((minutes=$minutes+$1)) # $1 son los minutos que teníamos originalmente, ahora le sumammos las horas que pasamos a minutos antes

    # Una vez que tenemos los minutos, vemos a cuantos días equivalen.
	if [ $minutes -ge 1440 ] # Comparamos pensando en que 1440 es un día, para saber si es más de un día con el greather/equal
	then
		((days=$minutes/1440)) # Si se cumple la condición, dividimos entre 1440 para saber cuántos días son.
		((minutes=$minutes-(($days*1440)))) # Saber cuantos minutos sobran, aquellos que no llegan a formar un día.
        # Ejemplo en 1499 minutos, esto da 1 día más 59 minutos que sobran. Lo que saca esta linea son esos 59 minutos.
	else
		days=0 # Si no son más de 1440, sabemos que son cero días (días completos)
	fi
    
    # Ahora trabajamos con los minutos que que nos sobraron arriba
	if [ $minutes -lt 60 ] # Si los minutos son menos de 60 (less than) 
	then
		hour=0 # entonces son cero horas
		min=$minutes # los minutos que no forman horas, se guardan en "min"
	else
		((hour=$minutes/60)) # para saber cuantashoras son esos minutos y guardarlos en la variable "hour"
		((min=$minutes%60)) # para saber cuantos minutos sobraron de esa división, y guardarlo en la variable "min"
	fi

    # Ahora mostramos el tiempo de conexión, la diferencia es si tenemos días o si tenemos solo horas y minutos, para mostrar distintos mensajes
	if [ $days -ge 1 ]  # ver si tenemos mayor o igual de un día
	then
		echo "El tiempo total de conexion es: $days dias, $hour horas y $min minutos" # Si la condición se cumple, se muestra esto
	else
		echo "El tiempo total de conexion es: $hour horas y $min minutos" # Si no tenemos días, mostramos este mensaje
	fi
}

## Se crea una función que dependiendo de si se le pasa o no un usuario en particular, obtiene todas las horas-minutos para luego pasarlas
## a la funcion converttime().
## Cuando se llama a la función gethoursminutes con un parametro $1, es porque la utilizamos para pasarle el username a filtrar con grep.
## De esta forma con la misma función pasamos las horas/minutos o de todos los usuarios o de uno solo en particular.
## Un ejemplo sería usar gethoursminutes $username
function gethoursminutes
{
    ## Definimos las variables de horas y de minutos en 0
    hourscount=0
    minutescount=0
    if [ $# -eq 1 ] && [ $1 == "reboot" ] ## Si se ingresa un solo parametro a la función gethoursminutes y ese parametro es reboot
                                          ## entonces lo que hacemos es filtrar en el grep para que me traiga las conexiones del usuario 
                                          ## (de existir) reboot y no las del system boot
    then
        hours=$(last | tr -s " " | egrep "^reboot [^s]" | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d":" -f1)
        minutes=$(last | tr -s " " | egrep "^reboot [^s]" | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    elif [ "$1" == "" ]# Si no ingresamos un usuario para filtrar, o sea, si $1 es nada.
    then
    ## Para guardar las horas y minutos, filtramos el last por todo lo que tenga ([0-9]*:[0-9]) de forma que eliminamos cualquier linea del last
    ## que diga "still logged in" (usuarios que sigan logueados) o que tenga más de 1 día de conexion (que aparecen como (1+23:44) por ejemplo).
    ## luego filtramos para quedarnos con lo de dentro de los () y para las horas nos quedamos con lo de la izquierda del : y para los
    ## minutos con lo de la derecha del :
    ## En caso de recibir el parametro $1 lo que hacemos es filtrar el last por el usuario recibido en ese parametro
    ## utilizando el grep grep "^$1 " (¿Por que un espacio después del $1, porque usamos tr -s " " delimitando cada columna por un espacio).
    ## el tr -s es trim con el separator " "
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d":" -f1) 
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    else # Si sí se le ingresó un usuario
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    fi
    ## En el for que suma todas las horas/minutos recibidos, utilizamos el sed para eliminar todos los ceros a la izquierda del valor
    ## porque bash no interpeta el 01 como un numero, solo el 1. Cuando tiene 0 a la izquierda no lo toma como valores que podamos sumar.
    for I in $hours # recorremos la lista hours con un for
    do
        I=$(echo $I | sed "s/^0*//g") # Sustituímos por nada todo los 0 que estén al principio.
        # "s/" "^0*" "/" "/g"
        # 1) "s/" , luego lo que queremos reemplazar. En este caso, es que empiece en cero y se repita n veces.
        # 2) otra barra, seguido de con qué lo queremos reemplazar.
        # 3) el "/g" es de global, porque se aplica a toda la lista que recorremos reemplazando.
        hourscount=$(($I+$hourscount)) # vamos sumando los valores que va tomando I y almacenandolo en hourscount
    done

    for I in $minutes # recorremos la lista minutes con un for
    do
        I=$(echo $I | sed "s/^0*//g") # hacemos lo mismo que en el for de hours
        minutescount=$(($I+$minutescount)) # sumamos igual que en hours y lo guardamos en minutescount
    done
    
    ## En caso de no obtener ninguna hora ni minuto a mostrar, es porque el usuario no tiene conexiones en el sistema, por ende devolvemos error.
    if [ "$hourscount" -eq 0 ] && [ "$minutescount" -eq 0 ] # si los valores de los dos for anteriores dan 0, entonces mostramos un error.
    then
        echo "No se han encontrado conexiones para listar en el sistema para el usuario $1.">&2 # Por letra, se redirecciona a la salida estándar de error.
        exit 0  # Pero como en realidad no es un error, sino un pedido de la letra, salimos con 0.
    else
        echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
        ## En este if validamos si debemos filtrar el last por el $1 (username) o no, antes de mostrar los valores y la suma de las horas/minutos
        if [ $# -eq 1 ] && [ $1 == "reboot" ]
        then
            last | grep "([0-9]*:[0-9]*)" | egrep "^reboot   [^s]"
        elif [ "$1" == "" ] # Si no se ingresó usuario (parámetro)
        then
            last | grep "([0-9]*:[0-9]*)" # Muestra solo las filas que tienen (HH:mm) y no las que tienen otras cosas como (1+HH:mm) o (15+HH:mm)

        else
            last | grep "([0-9]*:[0-9]*)" | grep "^$1 " # Sino, muestra solo las filas que tienen al usuario y tienen tiempo en formato (HH:mm)

        fi
        echo ""
        converttime $minutescount $hourscount
    fi
}

#########################################################################################################################################################################
############################################################# EL SCRIPT #################################################################################################
#########################################################################################################################################################################

## Si la persona no ingresa ningún parametro, le devolvemos el LAST pero con el cabezal (header|titulo) que usamos filtrando lo del
## "still logged in" o que tenga más de 1 día de conexion.
if [ $# -eq 0 ] # El $# es para comprobar la cantidad de parámetros que ingresamos. Si es cero, se cumple la condición que viene abajo
then
    echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
    last | grep "([0-9]*:[0-9]*)"
    exit 0
fi

## Con getops validamos lo introducido por el usuario, solicitando -r (puede ir solo), -u (acompañado de un valor, para eso el :)
## Luego lo que hacemos es guardar los valores que coincidan con lo ingresado en la variable opt
## Al saber que introdujo la persona, utilizamos case para poder gestionar las funciones del programa en base a esa misma variable opt
## Cada vez que la variable opt entra a un case, automaticamente se le hace un shift para pasar al siguiente valor de parametro introducido
while getopts ":ru:" opt;do # Mientras getops valide que hay una -r y/o -u username entonces pasan cosas.
                            # ":ru:"
                            # 1) Los ":" primeros son para que podamos editar los errores del getops (cambiar el mensaje de error)
                            # 2) El "ru" es para validar que ponga -r y/o -u username
                            # 3) El último ":" es para guardar el valor ingresado después del -u en $OPTARG

    case $opt in    # $opt como es un while, la primera vez que se ejecuta toma el valor del primer parámetro ingresado.
    ## Si la persona ingresa -r y SOLO -r ($# cantidad de paramentros = 1), entonces mostramos el last, con cabezales y con la suma de horas propia
    ## del -r
    r )
        if [ $# -eq 1 ]
        then
            gethoursminutes
            exit 0
#        else
#            sumahoras = true
        fi
        ;;
    ## Se ingresa al -u unicamente si la persona ingresa -u seguido del atributo a cargar para ese parametro (:). 
    ## Sigue de la mando de que debe ingresarse el -r antes, dado que en el case esta el r) antes que el u)
    ## Cuando la persona ingresa un atributo para un modificador (en este caso -u) se guarda en la variable $OPTARG, así que la usaremos como nuestro
    ## username o usuario a buscar.
    u )
        if ! validaruser $OPTARG
        then
            echo "No existe el usuario $OPTARG en el sistema.">&2
            exit 2
        else
            if [ $OPTARG == "reboot" ] # Agregamos esta linea para comprobar si se ingresó unicamente -u seguido del usuario (sin -r).
                                       # Se asegura que el primer parámetro sea la -u y el segundo sea algo que no empiece con un -
            then
                echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
                last | grep "([0-9]*:[0-9]*)" | egrep "^reboot   [^s]"
            else
                echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
                last | grep "([0-9]*:[0-9]*)" | grep "^$OPTARG "
            fi
        fi
        exit 0 
        ;;
    ## Este caso esta hecho porque si el modificador -u que tiene el (:) no recibe su atributo correspondiente, cae acá y controlamos esa excepción
    \: )    # Acá modificamos el mensaje de error del getops
        echo "No se ha especificado el usuario para el modificador -$OPTARG">&2
        exit 5
        ;;
    ## Getops guarda en la variable ? el valor del parametro (modificador -) que se introduzca que no pertenezca a las opciones, por ende 
    ## si se ingresa un parametro no valido, acá capturamos la excepción
    \? )    # 
        echo "Modificador -$OPTARG incorrecto. Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.">&2  # Se pide especificar así en la
                                                                                                                                    # letra, aunque si se puede ingresar
                                                                                                                                    # en orden diferente.
        exit 4
        ;;
    esac
done