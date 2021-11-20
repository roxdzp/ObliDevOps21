#!/bin/bash

## Funcion que valida que un usuario exista
function validaruser
{
	if ! grep -q "^$1:" /etc/passwd
	then
		return 1
	fi
}

## Esta funcion nos permite pasando dos parametros (hh y mm) convertir esas cantidades a dias, horas y minutos o a horas y minutos si dias = 0 (minutos < 1440)
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

## Se crea una función que dependiendo de si se le pasa o no un usuario en particular, obtiene todas las horas-minutos para luego pasarlas a la funcion converttime()
function gethoursminutes
{
    hourscount=0
    minutescount=0
    if [ "$1" == "" ]
    then
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    else
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$1 " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    fi
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
    if [ "$hourscount" -eq 0 ] && [ "$minutescount" -eq 0 ]
    then
        echo "No se han encontrado conexiones para listar en el sistema para el usuario $1.">&2
        exit 0
    else
        if [ "$1" == "" ]
        then
            echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
            echo ""
            converttime $minutescount $hourscount
        else
            echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)" | grep "^$1 "
            echo ""
            converttime $minutescount $hourscount
        fi
    fi
}
## Si la persona no ingresa ningún parametro, le devolvemos el LAST pero con el cabezal (header|titulo) que usamos
if [ $# -eq 0 ]
then
    echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
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
            gethoursminutes $OPTARG
            exit 0
        fi
        exit 0 
        ;;
    ## Este caso esta hecho porque si el modificador -u que tiene el (:) no recibe su atributo correspondiente, cae acá y controlamos esa excepción
    \: )
        echo "No se ha especificado el usuario para el modificador -u.">&2
        exit 5
        ;;
    ## Getops guarda en la variable ? el valor del parametro (modificador -) que se introduzca que no pertenezca a las opciones, por ende 
    ## si se ingresa un parametro no valido, acá capturamos la excepción
    \? )
        echo "Modificador $1 incorrecto. Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.">&2
        exit 4
        ;;
    esac
done