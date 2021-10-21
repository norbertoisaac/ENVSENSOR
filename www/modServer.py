#! /usr/bin/python3
if __name__=='__main__':
  import json
  import sys
  import os
  exitCode=1
  home='/var/lib/envsensor'
  serversFName=home+'/sensores.json'
  if len(sys.argv)==3:
    cmd=sys.argv[1]
    if cmd=='add':
      fName=sys.argv[2]
      if os.path.exists(fName):
        try:
          # validando la configuracion de nuevo sensor
          exitCode=2
          f1=open(fName,'r')
          jsonF=json.load(f1)
          f1.close()
          exitCode=3
          # agregando el nuevo
          serversF=open(serversFName,'r')
          servers=json.load(serversF)
          serversF.close()
          match=False
          for server in servers:
            if server['hostname']==jsonF['hostname']:
              match=True
              break
          if not match:
            servers.append(jsonF)
            serversF=open(serversFName,'w')
            json.dump(servers,serversF)
            serversF.close()
            estado={
              'name':jsonF['hostname'],
              'ultimoContactoEpoch':0,
              'ultimoContacto':'',
              'variables':[]
            }
            for variable in jsonF['variables']:
              estado['variables'].append({
                'nombre':variable['nombre'],
                'estado':None,
                'primerEstado':None,
                'primerEvento':0,
                'alarmado':False,
                'ultimoEstado':None,
                'ultimoValor':0,
                'ultimaCriticidad':None
              })
            estadoFName=home+'/log/'+jsonF['hostname']+'.estado.json'
            f1=open(estadoFName,'w')
            json.dump(estado,f1)
            f1.close()
            print(estadoFName)
          exitCode=0
          # agregando el archivo de estado
        except Exception as e:
          print(e)
        #else:
        #  pass
    elif cmd=='rm':
      sName=sys.argv[2]
      serversF=open(serversFName,'r')
      servers=json.load(serversF)
      serversF.close()
      for i in range(len(servers)):
        server=servers[i]
        if server['hostname']==sName:
          servers.pop(i)
          serversF=open(serversFName,'w')
          json.dump(servers,serversF)
          serversF.close()
          estadoFName=home+'/log/'+sName+'.estado.json'
          if os.path.exists(estadoFName):
            os.unlink(estadoFName)
          break
  quit(exitCode)
