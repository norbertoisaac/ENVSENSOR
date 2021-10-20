#! /usr/bin/python
permanenciaPorDefecto=300
tiempoMaximoParaNotificar=600
home='/var/lib/envsensor'
logPath=home+'/log'
sensoresFp=home+'/sensores.json'
import json
def notificarEventos():
  import time
  import sys
  #/var/lib/ntf/
  sys.path.append('/var/lib/ntf')
  import notification
  notificaciones=[]
  now=time.time()
  # Sensores
  f1=open(sensoresFp,'r')
  sensores=json.load(f1)
  f1.close()
  # Notificaciones
  notificacionesCP=home+'/'+'notificaciones.json'
  f1=open(notificacionesCP,'r')
  notificacionesC=json.load(f1)
  f1.close()
  import os
  for sensor in sensores:
    sensorEstadoFP=logPath+'/'+sensor['hostname']+'.estado.json'
    if os.path.exists(sensorEstadoFP):
      # leer el estado de las variables
      f1=open(sensorEstadoFP,'r')
      sensorEstado=json.load(f1)
      f1.close()
      for variableEstado in sensorEstado['variables']:
        if variableEstado['alarmado']:
	  if (now - variableEstado['primerEvento']) < tiempoMaximoParaNotificar:
	    criticidad=variableEstado['ultimaCriticidad']
	    ultimoContacto=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(variableEstado['primerEvento']))
	    for dst in notificacionesC['destinatarios']:
	      if dst['criticidad']==criticidad:
		email={}
		email['cuerpo']='<html><head></head><body><table>'
		email['cuerpo']+=notification.printDictToHtmlTable({'Hostname':sensor['hostname'],'Estado': variableEstado['ultimoEstado'],'Variable':variableEstado['nombre'],'Valor actual':str(variableEstado['ultimoValor']/10.0),'Primera incidencia':ultimoContacto})
		email['cuerpo']+='</body></html>'
		email['prioridadAlta']=True
		email['contenidoHTML']=True
		email['destinatarios']=dst['dstTpl']
		email['asunto']=variableEstado['ultimoEstado']+' '+sensor['hostname']
		notificaciones.append(
		  {
		    'tipo':'email',
		    'mensajes':[email]
		  }
		)
		sms={}
		sms['destinatarios']=dst['dstTpl']
		sms['cuerpo']=variableEstado['ultimoEstado']+' '+sensor['hostname']+', '+variableEstado['nombre']+' '+str(variableEstado['ultimoValor']/10.0)+', '+ultimoContacto
		notificaciones.append(
		  {
		    'tipo':'sms',
		    'mensajes':[sms]
		  }
		)
		break
	  variableEstado['alarmado']=False
	  variableEstado['primerEstado']=variableEstado['ultimoEstado']
	  variableEstado['primerEvento']=sensorEstado['ultimoContactoEpoch']
      # guardar las configuraciones
      f1=open(sensorEstadoFP,'w')
      json.dump(sensorEstado,f1)
      f1.close()
  # Enviar notificaciones
  if len(notificaciones):
    notification.enviarNotificaciones(notificaciones)
  return notificaciones
def generarEventos():
  f1=open(sensoresFp,'r')
  sensores=json.load(f1)
  f1.close()
  import os
  for sensor in sensores:
    sensorEstadoFP=logPath+'/'+sensor['hostname']+'.estado.json'
    if os.path.exists(sensorEstadoFP):
      f1=open(sensorEstadoFP,'r')
      sensorEstado=json.load(f1)
      f1.close()
      for variableEstado in sensorEstado['variables']:
	for variableSensor in sensor['variables']:
	  if variableEstado['nombre']==variableSensor['nombre']:
	    criticidad="error"
	    estado="Error"
	    for umbral in variableSensor['umbrales']:
	      umbralValor=umbral['valor']*10
	      if variableEstado['ultimoValor']>=umbralValor:
		criticidad=umbral['criticidad']
		estado=umbral['estado']
	    variableEstado['ultimoEstado']=estado
	    variableEstado['ultimaCriticidad']=criticidad
	    if variableEstado['ultimoEstado']==variableEstado['primerEstado'] or variableEstado['primerEstado']==None:
	      variableEstado['primerEstado']=estado
	      variableEstado['primerEvento']=sensorEstado['ultimoContactoEpoch']
	      variableEstado['alarmado']=False
	    elif (sensorEstado['ultimoContactoEpoch']-variableEstado['primerEvento'])>=permanenciaPorDefecto:
	      variableEstado['alarmado']=True
      #print sensorEstado
      f1=open(sensorEstadoFP,'w')
      json.dump(sensorEstado,f1)
      f1.close()
  return
# Generar los eventos
generarEventos()
notificaciones=notificarEventos()
#print notificaciones
