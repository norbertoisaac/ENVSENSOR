#! /bin/bash
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
  echo $tmpFile
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
  vim $tmpFile
  #jsonlint-php $tmpFile
  #if [[ $? -eq 0 ]]
  #then
  #  echo "validacion ok"
  #fi
  rm $tmpFile
elif [[ $1 == "rm" ]]
then
  echo "es rm"
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
