#! /usr/bin/python
import cgi
import psycopg2
import os
import sys
form = cgi.FieldStorage()
body = 'OK OK '
#conn = psycopg2.connect('dbname=sensor user=agent password=%Rn/74gR% host=10.150.31.69')
#cur = conn.cursor()
statusFile='/var/www/html/cgi-script/sensor/sensoresStatus.json'
#baseDir='/var/www/html/cgi/sensor1'
baseDir='/var/www/html/cgi-script/sensor'
logDir=baseDir+'/log'
rtype = ''
if 'rtype' in form:
  rtype = form.getvalue('rtype')
if rtype == 'sample':
  sampletime = form.getvalue('sampletime')
  name = form.getvalue('name')
  latitude = form.getvalue('latitude')
  longitude = form.getvalue('longitude')
  temperature = form.getvalue('temperature')
  humidity = form.getvalue('humidity')
  status = form.getvalue('status')
  message = form.getvalue('message')
  if status=='0':
    # Actualizar el estatus
    # Primero verificar si existe el archivo de estado del sensor
    import os
    estadoFPath=logDir+'/'+name+'.estado.json'
    if os.path.exists(estadoFPath):
      import time
      import json
      f1=open(estadoFPath,'r')
      estado=json.load(f1)
      f1.close()
      estado['ultimoContactoEpoch']=time.time()
      estado['ultimoContacto']=time.ctime()
      for i in range(len(estado['variables'])):
        if estado['variables'][i]['nombre']=='t1':
          estado['variables'][i]['ultimoValor']=int(temperature)
        elif estado['variables'][i]['nombre']=='h1':
          estado['variables'][i]['ultimoValor']=int(humidity)
      f1=open(estadoFPath,'w')
      json.dump(estado,f1)
      f1.close()
  # Insertar en la DB
  sql = "INSERT INTO temp_and_humd_log (name,lat,long,sampletime,status,message,temperature,humidity) VALUES ('"+name+"',"+latitude.replace(',','.')+","+longitude.replace(',','.')+",'"+sampletime+"',"+status+",'"+str(message)+"',"+temperature+","+humidity+")"
  try:
    import dbconn
    if dbconn.inres != 0:
      quit()
    conn = dbconn.conn
    cur = dbconn.cur
    cur.execute(sql)
    conn.commit()
  except psycopg2.DataError as e:
    body += str(e)
  except psycopg2.ProgrammingError as e:
    body += str(e)
  body += sql
# Print Response
status=200
message="OK"
headers = 'Content-Type: text/plain; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
