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
## Funcion a la que le pasamos el parametro usuario y sumvalue (-r) para devolvernos lo referente a ese usuario con su -r de ser necesario o unicamente el -r si es el caso
## Se realiza un case para cada situación, dependiendo de la cantidad de parametros introducidos.
case $# in
	## Si no se ingresan parametros se ejecuta el LAST con cabezales (headers)
	0)
		 echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
	;;
	## Si se ingresa solo un parametro, se sobreentiende que solo puede ser -r
	1)
		if [ "$1" == "-r" ]
                then
                        echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
			echo ""
			hourscount=0
       			hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f1)
       			for I in $hours
       			do
       				hourscount=$(($hourscount+$I))
       			done
			minutescount=0
       			minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
        		for I in $minutes
        		do
					regex="^[0][1-9]"
					regex2="^[0][0]"
					regex3="^[1-9][1-9]"
					if [[ "$I" =~ $regex ]]
					then
						I=$(echo "$I" | sed "s/0//g")
						minutescount=$(($minutescount+$I))	
					elif [[ "$I" =~ $regex2 ]]
					then
						I=$I
					elif [[ "$I" =~ $regex3 ]]
					then
						minutescount=$(($minutescount+$I))
					fi
        		done
			converttime $minutescount $hourscount
			exit 0
                else
			echo "Modificador $1 incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes.">&2
			exit 4
		fi
	;;
	## Si se ingresan 2 parametros se sobreentiende que solo pueden ser -u seguido del username, por lo que se valida que el primero sea -u y el siguiente sea un valor de usuario.
	2)
		if [ $1 == "-u" ]
        	then
                	echo "Buscado que el usuario exista..."
        	else
                	echo "Modificador $1 incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes.">&2
			exit 4
        	fi
        	user=$2
		if [ "$user" == "" ]
        	then
                	echo "No se ha especificado el usuario para el modificador -u">&2 | exit 1
        	else
			if ! validaruser $user
			then
			        echo "No existe el usuario $user en el sistema.">&2 | exit 2
			else
			        echo "El usuario $user existe, comprobando LAST"
			        echo "---------------------------------------"
			        echo ""
				echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)"
			        exit 0
			fi
		fi
	;;
	## Se sobreentiende que para pasar 3 parametros, estamos obligados a que sean -u -r y el username correspondiente, por lo que buscamos que se cumplan esas 3 cosas y en caso de que algo no se cumpla reportamos el error
	## Si no se cumplen esas 3 condiciones de los parametros, entonces obtenemos que $paramerror= el parametro que no cumple esa condición y avisame que hay un error.
	3)
		paramerror=""
		regex="^[^-]"
		if [ "$1" == "-r" ]
		then
			paramsum="true"
		else
			paramerror="$1"
		fi
		if [ "$2" == "-u" ]
		then
			paramuser="true"
		else
			paramerror="$2"
		fi
		if [[ "$3" =~ $regex ]]
		then
			paramname="$3"
		else
			paramerror="$3"
		fi
		if [ "$paramerror" != "" ]
		then
			echo "Modificador $paramerror incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes.">&2 | exit 4
		fi
		if [ "$paramuser" == "true" ] && [ "$paramsum" == "true" ] && [ "$paramname" != "" ]
		then
			if ! validaruser $paramname
                        then
                                echo "No existe el usuario $paramname en el sistema.">&2 | exit 2
                        else
                                echo "El usuario $paramname existe, comprobando LAST"
                                echo "---------------------------------------"
                                echo ""
                                hours=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$paramname " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f1)
	                        hourscount=0
				for I in $hours
	                        do
	                        	hourscount=$(($hourscount+$I))
	                        done
				minutescount=0
	                        minutes=$(last | tr -s " " | grep "([0-9]*:[0-9]*)" | grep "^$paramname " | cut -d"(" -f2 | cut -d")" -f1 | cut -d":" -f2)
	                        for I in $minutes
	                        do
								regex="^[0][1-9]"
								regex2="^[0][0]"
								regex3="^[1-9][1-9]"
								if [[ "$I" =~ $regex ]]
								then
									I=$(echo "$I" | sed "s/0//g")
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
			                echo "No se han encontrado conexiones para listar en el sistema para el usuario $paramname.">&2 | exit 0
			        else
					echo -e "Usuario\t Term\t      HOST\t       Fecha\t  H.Con\t  H.Des\t T.Con" | column -t -s"\t" && last | grep "([0-9]*:[0-9]*)" | grep "^$paramname "
                                	echo ""
					converttime $minutescount $hourscount
				fi
				exit 0
	        fi
		fi
	;;
	## Para cualquier otra cantidad de parametros distinta del 0 al 3 que no esta permitida, se avisa que la cantidad de parametros es erronea.
	*)
		echo "Cantidad de parámetros errónea, solo se aceptan los modificadores -r y -u (seguido de un nombre de usuario).">&2 | exit 3
	;;
esac
exit 0