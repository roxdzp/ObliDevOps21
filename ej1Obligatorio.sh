#!/bin/bash

## Funcion que valida que un usuario exista
function validaruser
{
    ## Utilizamos -q para que grep no escriba en pantalla y utilizamos la regex=^$1: que nos busca el parametro 
    ## recibido de la funcion en el archivo
    ## solo si empieza con ese parametro $1 y esta acompañado de un : al final.
	if ! grep -q "^$1:" /etc/passwd
	then
		return 1
	fi
}

## Esta funcion nos permite pasando dos parametros (hh y mm) convertir esas cantidades a dias, horas y minutos
## o a horas y minutos si los dias = 0 (minutos < 1440)
## Se debe de entender que 1440 minutos son 1 día y que 60 minutos son 1 hora.
function converttime
{
	((minutes=$2*60))
	((minutes=$minutes+$1))
	if [ $minutes -ge 1440 ]
	then
		((days=$minutes/1440))
		((minutes=$minutes-(($days*1440))))
	else
		days=0
	fi
	if [ $minutes -lt 60 ]
	then
		hour=0
		min=$minutes
	else
		((hour=$minutes/60))
		((min=$minutes%60))
	fi
	if [ $days -ge 1 ]
	then
		echo "El tiempo total de conexion es: $days dias, $hour horas y $min minutos"
	else
		echo "El tiempo total de conexion es: $hour horas y $min minutos"
	fi
}

## Se crea una función que dependiendo de si se le pasa o no un usuario en particular, obtiene todas las horas-minutos para luego pasarlas
## a la funcion converttime()
## Cuando se llama a la función convertime con un parametro $1, es porque la utilizamos para pasarle el username a filtrar con grep
## De esta forma con la misma función pasamos las horas/minutos o de todos los usuarios o de uno solo en particular.
## Un ejemplo sería usar converttime $username
function gethoursminutes
{
    hourscount=0
    minutescount=0
    if [ $# -eq 1 ] && [ $1 == "reboot" ]
    then
        hours=$(last | tr -s " " | egrep "^reboot [^s]" | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d":" -f1)
        minutes=$(last | tr -s " " | egrep "^reboot [^s]" | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    elif [ "$1" == "" ]
    then
    ## Para guardar las horas y minutos, filtramos el last por todo lo que tenga ([0-9]*:[0-9]) de forma que eliminamos cualquier linea del last
    ## que diga "still logged in" o que tenga más de 1 día de conexion.
    ## luego filtramos para quedarnos con lo de dentro de los () y para las horas nos quedamos con lo de la izquierda del : y para los minutos con
    ## lo de la derecha del :
    ## En caso de recibir el parametro $1 lo que hacemos es filtrar el last por el usuario recibido en ese parametro
    ## utilizando el grep grep "^$1 " (¿Por que un espacio después del $1, porque usamos tr -s " " delimitando cada columna por un espacio).
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    else
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    fi
    ## En el for que suma todas las horas/minutos recibidos, utilizamos el sed para eliminar todos los ceros a la izquierda del valor
    ## porque bash no interpeta el 01 como un numero, solo el 1.
    for I in $hours
    do
        I=$(echo $I | sed "s/^0*//g")
        hourscount=$(($I+$hourscount))
    done
    for I in $minutes
    do
        I=$(echo $I | sed "s/^0*//g")
        minutescount=$(($I+$minutescount))
    done
    ## En caso de no obtener ninguna hora ni minuto a mostrar, es porque el usuario no tiene conexiones en el sistema, por ende devolvemos error.
    if [ "$hourscount" -eq 0 ] && [ "$minutescount" -eq 0 ]
    then
        echo "No se han encontrado conexiones para listar en el sistema para el usuario $1.">&2
        exit 0
    else
        echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
        ## En este if validamos si debemos filtrar el last por el $1 (username) o no, antes de mostrar los valores y la suma de las horas/minutos
        if [ $# -eq 1 ] && [ $1 == "reboot" ]
        then
            last | grep "([0-9]*:[0-9]*)" | egrep "^reboot   [^s]"
        elif [ "$1" == "" ]
        then
            last | grep "([0-9]*:[0-9]*)"
        else
            last | grep "([0-9]*:[0-9]*)" | grep "^$1 "
        fi
        echo ""
        converttime $minutescount $hourscount
    fi
}
## Si la persona no ingresa ningún parametro, le devolvemos el LAST pero con el cabezal (header|titulo) que usamos filtrando lo del
## "still logged in" o que tenga más de 1 día de conexion.
if [ $# -eq 0 ]
then
    echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
    last | grep "([0-9]*:[0-9]*)"
    exit 0
fi
## Con getops validamos lo introducido por el usuario, solicitando -r (puede ir solo), -u (acompañado de un valor, para eso el :)
## Luego lo que hacemos es guardar los valores que coincidan con lo ingresado en la variable opt
## Al saber que introdujo la persona, utilizamos case para poder gestionar las funciones del programa en base a esa misma variable opt
## Cada vez que la variable opt entra a un case, automaticamente se le hace un shift para pasar al siguiente valor de parametro introducido
while getopts ":ru:" opt;do
    case $opt in
    ## Si la persona ingresa -r y SOLO -r ($# cantidad de paramentros = 1), entonces mostramos el last, con cabezales y con la suma de horas propia
    ## del -r
    r )
        if [ $# -eq 1 ]
        then
            gethoursminutes
            exit 0
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
            if [ $# -eq 3 ] && [ $1 == "-r" ] && [ $2 == "-u" ]
            then
                gethoursminutes $OPTARG
                exit 0
            else
                if [ $OPTARG == "reboot" ]
                then
                    echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
                    last | grep "([0-9]*:[0-9]*)" | egrep "^reboot   [^s]"
                else
                    echo -e "Usuario  Term         HOST             Fecha      H.Con   H.Des  T.Con"
                    last | grep "([0-9]*:[0-9]*)" | grep "^$OPTARG "
                fi
            fi
        fi
        exit 0
        ;;
    ## Este caso esta hecho porque si el modificador -u que tiene el (:) no recibe su atributo correspondiente, cae acá y controlamos esa excepción
    \: )
        echo "No se ha especificado el usuario para el modificador -$OPTARG">&2
        exit 5
        ;;
    ## Getops guarda en la variable ? el valor del parametro (modificador -) que se introduzca que no pertenezca a las opciones, por ende 
    ## si se ingresa un parametro no valido, acá capturamos la excepción
    \? )
        echo "Modificador -$OPTARG incorrecto. Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.">&2
        exit 4
        ;;
    esac
done