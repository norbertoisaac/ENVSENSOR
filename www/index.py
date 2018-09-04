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
form = cgi.FieldStorage()
if 'menu' in form:
  menu=form.getvalue('menu')
else:
  menu = ''
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
    <a class="menu" href="?menu=charts" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;
'''
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
if menu=='charts':
  import charts
  body += charts.getAllCharts(dbconn.conn,dbconn.cur)
elif menu=='devices':
  import devices
  if 'addDevice' in form:
    dev = {'name':'','active':True,'muteNoti':False,'twt':0,'tct':0,'hwt':0,'hct':0}
    dev['name'] = form.getvalue('deviceName')
    dev['active'] = form.getvalue('deviceActive')
    dev['muteNoti'] = form.getvalue('deviceMuteNoti')
    dev['twt'] = form.getvalue('tempWarning')
    dev['tct'] = form.getvalue('tempCritical')
    dev['hwt'] = form.getvalue('humidityWarning')
    dev['hct'] = form.getvalue('humidityCritical')
    devices.addDevice(dev)
    body += '<h1>'+str(dev)+'</h1>'
  body += devices.getAllDevicesHtml(dbconn.conn,dbconn.cur)
  #import graph
  #import base64
  #graph.graph_draw(dbconn.conn,dbconn.cur,'MSCFDO-Sala2')
  #body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  #graph.graph_draw(dbconn.conn,dbconn.cur,'MSCFDO-Sala1')
  #body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  #graph.graph_draw(dbconn.conn,dbconn.cur,'MSCCDE-Sala1')
  #body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
body+='''
  </div>
  </body>
</html>
'''
headers = 'Content-Type: text/html; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
