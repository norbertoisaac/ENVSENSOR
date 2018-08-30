#! /bin/bash
localT=0
localH=0
while true
do
  . /var/lib/radmin/log/res
  if [ $status -eq 0 ]
  then
    localT=$temperature
    localH=$humidity
  fi
  echo "Hola $localH 1"
  python /var/lib/radmin/bin/rpi7seg.py $localH 1
  echo "Hola $localT 5"
  python /var/lib/radmin/bin/rpi7seg.py $localT 5
  #break
done
