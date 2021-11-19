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

if [ $# -eq 0 ]
then
    echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
    exit 0
fi

while getopts "ru:" opt
   do
     case $opt in
        r )
            if [ $# -eq 1 ]
            then
                gethoursminutes
                exit 0
            fi
        ;;
        u )
            if [ $# -eq 3 ]
            then
                if ! validaruser $OPTARG
                then
                    echo "No existe el usuario $OPTARG en el sistema.">&2
                    exit 2
                else
                    gethoursminutes $OPTARG
                    exit 0
                fi
                exit 0
            else
                echo "Modificador $1 incorrecto. Solo se aceptan -r -u usuario, y en ese orden en caso de estar ambos presentes.">&2
                exit 4
            fi
        ;;
     esac
done