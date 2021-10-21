#! /bin/bash
home="/var/lib/envsensor"
if [[ $1 == "add" ]]
then
  echo -n "IP del sensor: "
  read ip
  echo -n "Hostname del sensor: "
  read hostname
  echo $ip $hostname
  echo "Introducir las variables:"
  echo -n "  Nombre de la variable: "
  read varName
  echo -n "  Tipo de variable (temperatura,humedad,etc): "
  read tipoDeVariable
  tmpFile=$(mktemp "${TMPDIR:-/tmp/}$(basename $0).XXXXXXXXXXXX.json")
  cat > $tmpFile <<HERE
{
  "hostname":"$hostname",
  "ip":"$ip",
  "coleccion":{
    "activo":true,
    "metodo":"pushWeb"
  },
  "variables":[
    {
      "nombre":"$varName",
      "tipo":"$tipoDeVariable",
      "unidadDeMedida":"",
      "descripcion":"",
      "medir":true,
      "rango":{
        "inferior":0.0,
        "superior":100.0
      },
      "umbrales":[
        {
          "valor":0.0,
          "operador":"ge",
          "estado":"Normal",
          "criticidad":"info"
        }
      ]
    }
  ]
}
HERE
  while true
  do
    vim $tmpFile
    estadoFN=$($home/modServer.py add $tmpFile)
    res=$?
    echo $res
    if [[ $res -eq 0 ]]
    then
      chmod 660 $estadoFN
      chown envsensor:www-data $estadoFN
      rm $tmpFile
      break
    elif [[ $res -eq 2 ]] # Falla en la sintaxis json
    then
      echo $estadoFN
      read
    elif [[ $res -eq 3 ]] # Falla al leer/escribir los archivos
    then
      echo $estadoFN
      read
      break
    else # Falla generica
      echo $estadoFN
      read
      break
    fi
  done
elif [[ $1 == "rm" ]]
then
  echo -n "Hostname del sensor: "
  read hostname
  if [[ $hostname != '' ]]
  then
    $home/modServer.py rm $hostname
  fi
elif [[ $1 == "mod" ]]
then
  echo "es mod"
else
  cat <<HERE
comandos disponibles:
	add
	  agregar un nuevo sensor
	rm
	  borrar un servidor
	mod
	  modificar un servidor
HERE
fi
