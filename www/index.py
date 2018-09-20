#! /usr/bin/python
import cgi
import sys
import dbconn
if dbconn.inres != 0:
  quit()
#graph.graph_format('pdf')
#graph.graph_draw()
#fname = open('reporteWelcome.pdf','w')
#fname.write(graph.body)
#fname.close()
body = ''
form = cgi.FieldStorage()
if 'menu' in form:
  menu=form.getvalue('menu')
else:
  menu = 'alarms'

if 'showFPDeviceId' in form:
  import graph
  deviceId = form.getvalue('showFPDeviceId')
  imageBase64 = graph.getDeviceFPBase64(dbconn.conn,dbconn.cur,dbconn.imagesDB,deviceId)
  body += '''<html><body>
  '''
  if imageBase64:
    body += '<image style="margin-left:auto;margin-right:auto;display:block;" src="data:image/png;base64,'+imageBase64+'">'
  else:
    body += '<h1 style="text-align:center;color:white;">This device does not have floorplan image</h1>'
  body += '</body></html>'
  headers = 'Content-Type: text/html; charset=utf-8\r\n'
  headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
  sys.stdout.write(headers+body)
  quit()

body = '''<!DOCTYPE html>
<html>
  <head>'''

if menu == 'charts':
  body += '<meta http-equiv="refresh" content="10">'
body +='''
    <title>EnvSensor</title>
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
      <h style="font-size:300%;text-align:center;">Environment status</h>
    </div>
    <!-- MENU -->
    <div style="background-color:#5f5f5f;height:30px">
'''
# Menu
body += '<a class="menu" href="?menu=alarms" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;'
if menu=='alarms':
  body += 'background-color:black;'
body += '">ALARMS</a>'
body += '<a class="menu" href="?menu=charts" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;'
if menu=='charts':
  body += 'background-color:black;'
body += '">CHARTS</a>'
body += '<a class="menu" href="?menu=devices" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;'
if menu=='devices':
  body += 'background-color:black;'
body += '">DEVICES</a>'
body += '''<!-- <a class="menu" href="?menu=sqltpl" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">QUERY TEMPLATES</a> -->
      <!-- <select style="height:100%;background-color:gray;" form="formsubg" name="menu" onchange="selectsubg()">
        <option >Charts</option>
        <option value="views">Views</option>
        <option value="sqltpl">SQL templates</option>
        <option value="counters">Counters</option>
      </select>-->
      <a class="menu" href="mailto:" style="float:right;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">Support request</a>
    </div>
  </div>
  <div style="background-color:#e6e6e6;width:100%;position:fixed;top:100px;bottom:0px;overflow-y:auto">'''

# Alarms menu content
if menu=='alarms':
  import alarms
  if 'searchAlarm' in form:
    body += str(form)
  body += '<br><div style="float:left;display:block;"><span style="color:black;"></span><form id="filterAlarm" method="post"><span style="font-weight: bold;">Filter:  </span>Device<select name="deviceId"><option value="---">All</option>'
  import devices
  devs = devices.getAllDevices(dbconn.conn,dbconn.cur)
  for dev in devs:
    body += '<option value="'+str(dev['id'])+'">'+dev['name']+'</option>'
  body += '</select> Severity<select name="sev"><option value="5">Notice</option><option value="4">Warning</option><option value="3">Minor</option><option value="2" selected>Major</option><option value="1">Critical</option></select> Active<select name="active"><option value="--">All</option><option value="t">Yes</option><option value="f">No</option></select> Acknowledged<select name="ack"><option value="--">All</option><option value="t">Yes</option><option value="f">No</option></select> Count<input name="count" value="100" type="number" style="width:55px"> <input type="submit" name="searchAlarm" value="Search" style="background-color:yellow"></form></div>'

# Charts menu content
if menu=='charts':
  import charts
  body += charts.getAllCharts(dbconn.conn,dbconn.cur)

# Devices menu content
if menu=='devices':
  import devices
  import time
  import os
  #body += '<h1>'+str(os.environ)+'</h1>'

  if 'addDevice' in form:
    dev = {'name':'','active':True,'muteNoti':True,'floorPlan':None,'twt':0,'tct':0,'hwt':0,'hct':0}
    dev['name'] = form.getvalue('deviceName')
    if form.getvalue('deviceActive') == None:
      dev['active'] = False
    if form.getvalue('deviceMuteNoti') == None:
      dev['muteNoti'] = False
    dev['twt'] = float(form.getvalue('tempWarning'))*10
    dev['tct'] = float(form.getvalue('tempCritical'))*10
    dev['hwt'] = float(form.getvalue('humidityWarning'))*10
    dev['hct'] = float(form.getvalue('humidityCritical'))*10
    if 'deviceFP' in form:
      import random
      dev['floorPlan'] = str(time.time())+'-'+str(random.randint(1,101)*12345)+'.png'
      #f = open(dev['floorPlan'],'w')
      #f.write(form['deviceFP'])
      #f.close()
      #body += '<p>'+str(form['deviceFP'].value)+'</p>'
      if form['deviceFP'].file:
        f = open(dbconn.imagesDB+'/'+dev['floorPlan'],'w')
	f.write(form['deviceFP'].file.read())
	f.close()
    devices.addDevice(dev,dbconn.conn,dbconn.cur)
    #body += '<h1>'+str(form)+'</h1>'
    #body += '<h1>'+str(dev)+'</h1>'
    #body += cgi.print_form(form)
  if 'modDevice' in form:
    dev = {'id':None,'active':True,'muteNoti':True,'floorPlan':None,'twt':0,'tct':0,'hwt':0,'hct':0}
    dev['id'] = int(form.getvalue('devId'))
    if form.getvalue('deviceActive') == None:
      dev['active'] = False
    if form.getvalue('deviceMuteNoti') == None:
      dev['muteNoti'] = False
    dev['twt'] = float(form.getvalue('tempWarning'))*10
    dev['tct'] = float(form.getvalue('tempCritical'))*10
    dev['hwt'] = float(form.getvalue('humidityWarning'))*10
    dev['hct'] = float(form.getvalue('humidityCritical'))*10
    if form['deviceFP'].value != '':
      import random
      dev['floorPlan'] = str(time.time())+'-'+str(random.randint(1,101)*12345)+'.png'
      if form['deviceFP'].file:
        f = open(dbconn.imagesDB+'/'+dev['floorPlan'],'w')
	f.write(form['deviceFP'].file.read())
	f.close()
    devices.modDevice(dbconn.imagesDB,dev,dbconn.conn,dbconn.cur)
    #body += '<h1>'+str(form)+'</h1>'
    #body += '<h1>'+str(dev)+'</h1>'
  if 'rmvDevice' in form:
    dev = {'id':None,'active':True,'muteNoti':True,'floorPlan':None,'twt':0,'tct':0,'hwt':0,'hct':0}
    dev['id'] = int(form.getvalue('devId'))
    devices.rmvDevice(dbconn.imagesDB,dev,dbconn.conn,dbconn.cur)
  body += devices.getAllDevicesHtml(dbconn.conn,dbconn.cur)
body+='''
  </div>
  </body>
</html>
'''
headers = 'Content-Type: text/html; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
