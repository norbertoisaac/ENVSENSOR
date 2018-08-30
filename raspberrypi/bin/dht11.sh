#! /bin/bash
touch /var/lib/radmin/log/serverResponse
while true
do
  if [ ! -f /var/lib/radmin/log/temperatureWarning ]
  then
    echo -n 0 > /var/lib/radmin/log/temperatureWarning
  fi
  if [ ! -f /var/lib/radmin/log/temperatureCritical ]
  then
    echo -n 0 > /var/lib/radmin/log/temperatureCritical
  fi
  if [ ! -f /var/lib/radmin/log/humidityWarning ]
  then
    echo -n 0 > /var/lib/radmin/log/humidityWarning
  fi
  if [ ! -f /var/lib/radmin/log/humidityCritical ]
  then
    echo -n 0 > /var/lib/radmin/log/humidityCritical
  fi
  if [ ! -f /var/lib/radmin/log/sensorUnavailable ]
  then
    echo -n 0 > /var/lib/radmin/log/sensorUnavailable
  fi
  day=$(date +"%Y%m%d")
  touch /var/lib/radmin/log/event_$day
  # Read configuration file
  . /var/lib/radmin/conf/main.conf
  # Collect sensor output
  /var/lib/radmin/bin/dht11 > /var/lib/radmin/log/res 2>/dev/null 2>/dev/null
  . /var/lib/radmin/log/res
  # Log result
  echo $(date +"%Y-%m-%d %H:%M:%S"),$status,$message,$temperature,$humidity >> /var/lib/radmin/log/event_$day
  # Post sample to server
  if [ $postResult == "YES" ]
  then
    post="rtype=sample&sampletime=$sampletime&name=$name&latitude=$latitude&longitude=$longitude&temperature=$temperature&humidity=$humidity&status=$status&message=$message"
    wget --server-response --timeout=5 --post-data="$post" $url -O /var/lib/radmin/log/serverResponse -o /var/lib/radmin/log/serverResponseError
    echo $post
  fi
  # Sensor unavailable warning
  if [ $status -eq 1 ]
  then
    if [ $(cat /var/lib/radmin/log/sensorUnavailable) == "0" ]
    then
      echo -n 1 > /var/lib/radmin/log/sensorUnavailable
      if [ $notifySensorNotResponding == "YES" ]
      then
	if [ $emailNotification == "YES" ]
	then
	  echo "Sensor unavailable" | mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Sensor unavailable. $name" $emailRecipents
	fi
	#if [ $webServiceNotification == "YES" ]
	#then
	#  #echo "Sensor unavailable. Sending email"
	#fi
      fi
    fi
  else
    if [ $(cat /var/lib/radmin/log/sensorUnavailable) == "1" ]
    then
      echo -n 0 > /var/lib/radmin/log/sensorUnavailable
      if [ $notifySensorNotResponding == "YES" ]
      then
	if [ $emailNotification == "YES" ]
	then
	  echo "Sensor available" | mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Sensor available. $name" $emailRecipents
	fi
	#if [ $webServiceNotification == "YES" ]
	#then
	#  #echo "Sensor unavailable. Sending email"
	#fi
      fi
    fi
  fi
  # Success sample
  if [ $status -eq 0 ]
  then
    # Temperature normal
    if [ $temperature -lt $temperatureWarning ]
    then
      if [[ $(cat /var/lib/radmin/log/temperatureWarning) == "1" || $(cat /var/lib/radmin/log/temperatureCritical) == "1" ]]
      then
        echo "Temperatura normal: $temperature"
	echo -n 0 > /var/lib/radmin/log/temperatureWarning
	echo -n 0 > /var/lib/radmin/log/temperatureCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Temperature normal. $name" $emailRecipents <<HERE
Temperature normal
Temperature: $(echo "scale=1;$temperature/10" | bc -l) °C

Sensor: $name
HERE
	  fi
	fi
      fi
    # Temperature warning
    elif [[ $temperature -ge $temperatureWarning && $temperature -lt $temperatureCritical ]]
    then
      if [[ $(cat /var/lib/radmin/log/temperatureWarning) == "0" && $(cat /var/lib/radmin/log/temperatureCritical) == "0" ]]
      then
        echo "Temperatura warning: $temperature > $temperatureWarning"
	echo -n 1 > /var/lib/radmin/log/temperatureWarning
	echo -n 0 > /var/lib/radmin/log/temperatureCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Temperature warning. $name" $emailRecipents <<HERE
Temperature warning
Temperature: $(echo "scale=1;$temperature/10" | bc -l) °C
Warning threshold: $(echo "scale=1;$temperatureWarning/10" | bc -l) °C

Sensor: $name
HERE
	  fi
	fi
      fi
    # Temperature critical
    elif [ $temperature -ge $temperatureCritical ]
    then
      if [ $(cat /var/lib/radmin/log/temperatureCritical) == "0" ]
      then
        echo "Temperatura critical: $temperature > $temperatureCritical"
	echo -n 0 > /var/lib/radmin/log/temperatureWarning
	echo -n 1 > /var/lib/radmin/log/temperatureCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Temperature critical. $name" $emailRecipents <<HERE
Temperature critical
Temperature: $(echo "scale=1;$temperature/10" | bc -l) °C
Critical threshold: $(echo "scale=1;$temperatureCritical/10" | bc -l) °C

Sensor: $name
HERE
	  fi
	fi
      fi
    fi
    # humidity normal
    if [ $humidity -lt $humidityWarning ]
    then
      if [[ $(cat /var/lib/radmin/log/humidityWarning) == "1" || $(cat /var/lib/radmin/log/humidityCritical) == "1" ]]
      then
        echo "Humidity normal: $humidity"
	echo -n 0 > /var/lib/radmin/log/humidityWarning
	echo -n 0 > /var/lib/radmin/log/humidityCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Humidity normal. $name" $emailRecipents <<HERE
Humidity normal
Humidity: $(echo "scale=1;$humidity/10" | bc -l) %

Sensor: $name
HERE
	  fi
	fi
      fi
    # Humidity warning
    elif [[ $humidity -ge $humidityWarning && $humidity -lt $humidityCritical ]]
    then
      if [[ $(cat /var/lib/radmin/log/humidityWarning) == "0" && $(cat /var/lib/radmin/log/humidityCritical) == "0" ]]
      then
        echo "Humidity warning: $humidity > $humidityWarning"
	echo -n 1 > /var/lib/radmin/log/humidityWarning
	echo -n 0 > /var/lib/radmin/log/humidityCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Humidity warning. $name" $emailRecipents <<HERE
Humidity warning
Humidity: $(echo "scale=1;$humidity/10" | bc -l) %
Warning threshold: $(echo "scale=1;$humidityWarning/10" | bc -l) %

Sensor: $name
HERE
	  fi
	fi
      fi
    # Humidity critical
    elif [ $humidity -ge $humidityCritical ]
    then
      if [ $(cat /var/lib/radmin/log/humidityCritical) == "0" ]
      then
        echo "Humidity critical: $humidity > $humidityCritical"
	echo -n 0 > /var/lib/radmin/log/humidityWarning
	echo -n 1 > /var/lib/radmin/log/humidityCritical
	if [ $notifyTheshold == "YES" ]
	then
	  if [ $emailNotification == "YES" ]
	  then
	    mailx -r $emailFrom -S smtp=$smtpServerAddress:$smtpServerPort -s "Humidity critical. $name" $emailRecipents <<HERE
Humidity critical
Humidity: $(echo "scale=1;$humidity/10" | bc -l) %
Critical threshold: $(echo "scale=1;$humidityCritical/10" | bc -l) %

Sensor: $name
HERE
	  fi
	fi
      fi
    fi
  fi
  #exit
  sleep $pollingInterval
done
