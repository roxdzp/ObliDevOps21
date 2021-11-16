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
		echo "El tiempo total de conexión es: $days días, $hour horas y $min minutos"
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
        hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$paramname " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f1)
        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$paramname " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
    fi
    for I in $hours
    do
        hourscount=$(($hourscount+$I))
    done
    for I in $minutes
    do
        regex="^[0][1-9]"
        regex2="^[0][0]"
        regex3="^[1-9][1-9]"
        if [[ "$I" =~ $regex ]]
        then
            I=$(echo "$I" | sed "s/^0*//g")
            minutescount=$(($minutescount+$I))	
        elif [[ "$I" =~ $regex2 ]]
        then
            I=$I
        elif [[ "$I" =~ $regex3 ]]
        then
            minutescount=$(($minutescount+$I))
        fi
    done
    if [ "$hourscount" -eq 0 ] && [ "$minutescount" -eq 0 ]
        then
                echo "No se han encontrado conexiones para listar en el sistema para el usuario $paramname.">&2
                exit 0
        else
        echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)" | grep "^$paramname "
        echo ""
        converttime $minutescount $hourscount
    fi
}

if [ $# -eq 0 ]
then
    echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
    exit 0
fi
if [ $# -eq 1 ] && [ "$1" == "-r" ]
then
    echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
    echo ""
    gethoursminutes
    exit 0
elif [ $# -gt 1 ] && [ "$1" == "-r" ]
then
    paramr="true"
    shift
else
    echo "Modificador $1 incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes.">&2
    exit 4
fi

if [ "$1" == "-u" ]
then
    paramu="true"
    shift
else
    echo "Modificador $1 incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes.">&2
    exit 4
fi

regex="^[^-]"
if [[ "$1" =~ $regex ]] && [ "$1" != "" ]
then
    paramname="$1"
    if ! validaruser $paramname
    then
            echo "No existe el usuario $user en el sistema.">&2
            exit 2
    fi
    shift
else
    echo "No se ha especificado el usuario para el modificador -u">&2
    exit 1
fi

if [ $# -ge 1 ]
then
    echo "Cantidad de parámetros errónea, solo se aceptan los modificadores -r y -u (seguido de un nombre de usuario).">&2
    exit 3
fi

if [ "$paramu" == "true" ] && [ "$paramr" == "true" ]
then
    echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)" | grep "^$paramname "
    echo ""
    gethoursminutes $paramname
fi
exit 0