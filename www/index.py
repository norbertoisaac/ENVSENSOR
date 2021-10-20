#! /usr/bin/python3
import cgi
import sys
home="/var/lib/envsensor"
sensoresF=home+"/sensores.json"
sensoresStatusF=home+"/sensoresStatus.json"
logDir=home+"/log"
form = cgi.FieldStorage()
body = '''<!DOCTYPE html>
<html>
<!-- Nucleo S.A.
   Autor: Norberto.Nunez@personal.com.py
   Copyright NUCLEO S.A. 2018
   Este es un script que despliega la pagina de estadisticas de los sensores
   -->
  <head>'''
if 'lapso' in form:
  lapso=form.getvalue('lapso')
else:
  lapso='24h'
if 'menu' in form:
  menu=form.getvalue('menu')
else:
  menu = 'charts'
  #menu = 'devices'
body +='''
    <title>Sensor</title>
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
    <script>
      function selectsubg(){
    document.forms["formsubg"].submit();
      }
      function submitformid(id){
        var form = document.getElementById(id);
    form.submit();
      }
      function newWindow(url){
    //document.forms["formsubg"].elements["subg"].value="all";
    //document.forms["formsubg"].submit();
      window.open(url, '_blank','menubar=no,status=no,titlebar=no,width=600px');
      }
      function togleDisplay(divid){
        var div = document.getElementById(divid);
    if(div.style.display == 'none')
    {
      div.style.display = 'block';
    }
    else
    {
      div.style.display = 'none';
    }
      }
      window.name = '';
      console.log(window.name);
    </script>
    <style type="text/css">
      #menubar a {padding:11px 15px 11px 15px;float:left;text-decoration:none;}
      /*#menubar a:link,a:visited {color:#f1f1f1;}*/
      #menubar a:hover,a:active {background-color:#ff4800;}
      table, table.tecspec {
    border-collapse: collapse;
    font-size: 100%;
    font-family: verdana,helvetica,arial,sans-serif;
    text-align: start;
    border-spacing: 2px;
    border-color: grey;
      }
      table.reference tr:nth-child(odd) {
    background-color: #F6F4F0;
      }
      table.reference th {
          color: #ffffff;
          background-color: #555555;
          border: 1px solid #555555;
          font-size: 12px;
          padding: 3px;
          vertical-align: top;
          text-align: left;
      }
    table.reference td {
      border: 1px solid #d4d4d4;
      padding: 5px;
      padding-top: 7px;
      padding-bottom: 7px;
      vertical-align: top;
    }
    a.menu:hover{
      background-color:black;
    }
    div.popupdiv {
      left: 0px;
      top: 0px;
      height: 100%;
      width: 100%;
      color: rgb(0, 0, 0);
      background-color: rgba(0, 0, 0, 0.4);
      z-index: 4;
      position: fixed;
      overflow: auto;
      padding-top: 0px;
    }
    div.insidepopup {
      padding: 0px;
      box-sizing: border-box;
      background-color: #FFF;
      position: relative;
      margin: auto;
      width: fit-content;
      width: -moz-fit-content;
      margin-top: 120px
    }
    </style>
  </head>
  <body style="margin:0;">
  <form id="formsubg" method="get" action="?" target="_top"></form>
  <div style="top:0;width:100%;height:100px;position:fixed">
    <!-- TOP NAV -->
    <div style="text-align:center;background-color:#6666ff;height:70px">
      <h style="font-size:300%;text-align:center;">Sensor status</h>
    </div>
    <!-- MENU -->
    <div style="background-color:#5f5f5f;height:30px">
      <a class="menu" href="?menu=charts" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">CHARTS</a>
      <a class="menu" href="?menu=devices" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">SENSORES</a>
      <!-- <a class="menu" href="?menu=sqltpl" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">QUERY TEMPLATES</a> -->
      <!-- <select style="height:100%;background-color:gray;" form="formsubg" name="menu" onchange="selectsubg()">
        <option >Charts</option>
        <option value="views">Views</option>
        <option value="sqltpl">SQL templates</option>
        <option value="counters">Counters</option>
      </select>-->
      <a class="menu" href="mailto:nunezno@personal.com.py" style="float:right;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">Soporte: Norberto N./SVA</a>
    </div>
  </div>
  <div style="background-color:#e6e6e6;width:100%;position:fixed;top:100px;bottom:0px;overflow-y:auto">'''
if menu=='charts':
  import dbconn
  conn,cur=dbconn.getDbConn()
  if not conn==None:
    body += '''<form id="formLapso" method="post" action="?menu=charts">
    <script>
    function sFormLapso(){
      var f=document.getElementById('formLapso');
      f.submit();
    }'''
    if lapso=='1h':
      body+='setTimeout(sFormLapso,60000);'
    body+='</script>'
    lapsos={'30d':{'o':1,'checked':False,'label':'1m'},'7d':{'o':2,'checked':False,'label':'7d'},'Ayer':{'o':3,'checked':False,'label':'Ayer'},'24h':{'o':4,'checked':False,'label':'24h'},'12h':{'o':5,'checked':False,'label':'12h'},'6h':{'o':6,'checked':False,'label':'6h'},'1h':{'o':7,'checked':False,'label':'1h (auto refresh)'}}
    if not lapso in lapsos:
      lapso='24h'
    lapsos[lapso]['checked']=True
    for l,v in sorted(lapsos.items(),key=lambda x: x[1]['o']):
      body+='<input type="radio" name="lapso" onclick="sFormLapso()" value="'+str(l)+'"'+' id="idInputLapso'+str(l)+'"'
      if lapsos[l]['checked']:
        body+='checked'
      body+='><label for="idInputLapso'+str(l)+'">'+v['label']+'</label>'
    body+='</form>'
    import graph
    import base64
    import json
    f1=open(sensoresF,'r')
    sensores=json.load(f1)
    f1.close()
    for sensor in list(map(lambda x: x['hostname'],sensores)):
      graph.graphconf(conn,cur,str(sensor),lapso)
      body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  else:
    body+='<p>Hay problemas de conexi&oacute;n contra la base de datos</p>'
elif menu=='devices':
  import json
  # Sensores
  f1=open(sensoresF,'r')
  sensores=json.load(f1)
  f1.close()
  # Status
  # Table
  body+='<h1>Sensores</h1><table class="reference notranslate"><tr><th>Sonda</th><th>IP</th><th>Recolecci&oacute;n</th><th>Variables</th><th>Estado</th></tr>'
  for sensor in sensores:
    body+='<tr>'
    body+='<td>'+sensor['hostname']+'</td>'
    body+='<td>'+sensor['ip']+'</td>'
    if sensor['coleccion']['activo']:
      recoleccion='<input type="checkbox" checked disabled>Habilitado'
    else:
      recoleccion='<input type="checkbox" disabled>Inhabilitado'
    recoleccion+='<br>M&eacute;todo '+sensor['coleccion']['metodo']
    body+='<td>'+recoleccion+'</td>'
    body+='<td>'
    for variable in sensor['variables']:
      body+=variable['nombre']+'<br>&emsp;Tipo: '+variable['tipo']+'<br>&emsp;Unidad de medida: '+variable['unidadDeMedida']+'<br>&emsp;Descripci&oacute;n: '+variable['descripcion']+'<br>&emsp;Umbrales:'
      for umbral in variable['umbrales']:
        body+='<br>&emsp;&emsp;'+str(umbral['valor'])+'=>'+umbral['estado']
      body+='<br>'
    body+='</td><td>'
    # estado
    import os
    sensorStatusFName=logDir+'/'+sensor['hostname']+'.estado.json'
    if os.path.exists(sensorStatusFName):
      f1=open(sensorStatusFName,'r')
      estatus=json.load(f1)
      f1.close()
      body+='&Uacute;ltima conexi&oacute;n: '+str(estatus['ultimoContacto'])
      for variable in estatus['variables']:
        body+='<br>'+variable['nombre']+': '+str(variable['ultimoValor']/10.0)+' => estado: '+str(variable['ultimoEstado'])
    body+='</td>'
    body+='</tr>'
  body+='</table>'
body+='''
  </div>
  </body>
</html>
'''
headers = 'Content-Type: text/html; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
