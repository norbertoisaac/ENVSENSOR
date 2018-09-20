def getDeviceFPImage(dev,conn,cur):
  sql = 'SELECT floorplanPosition FROM device WHERE id=%(id)s'
  cur.execute(sql,dev)
  imageName = cur.fetchone()['floorplanposition']
  return imageName

def addDevice(dev,conn,cur):
  if dev['floorPlan']:
    sql = "INSERT INTO device(name,active,floorplanPosition,muteAlarmsNotif,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) VALUES (%(name)s,%(active)s,%(floorPlan)s,%(muteNoti)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s)"
  else:
    sql = "INSERT INTO device(name,active,muteAlarmsNotif,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) VALUES (%(name)s,%(active)s,%(muteNoti)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s)"
  cur.execute(sql,dev)
  conn.commit()
  return

def rmvDeviceFPImageFile(baseDir,imageName):
  if imageName:
    import os
    os.unlink(baseDir+'/'+imageName)
  return

def rmvDeviceFPImage(baseDir,dev,conn,cur):
  imageName = getDeviceFPImage(dev,conn,cur)
  rmvDeviceFPImageFile(baseDir,imageName)
  return

def modDevice(baseDir,dev,conn,cur):
  if dev['floorPlan']:
    rmvDeviceFPImage(baseDir,dev,conn,cur)
    sql = "UPDATE device SET (active,muteAlarmsNotif,floorplanPosition,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) = (%(active)s,%(muteNoti)s,%(floorPlan)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s) WHERE id=%(id)s"
  else:
    sql = "UPDATE device SET (active,muteAlarmsNotif,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) = (%(active)s,%(muteNoti)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s) WHERE id=%(id)s"
  cur.execute(sql,dev)
  conn.commit()
  return

def rmvDevice(baseDir,dev,conn,cur):
  sql = "DELETE FROM device WHERE id=%(id)s AND active='f' RETURNING floorplanposition"
  cur.execute(sql,dev)
  conn.commit()
  if cur.rowcount == 1:
    imageName = cur.fetchone()['floorplanposition']
    rmvDeviceFPImageFile(baseDir,imageName)
  return

def getAllDevices(conn,cur):
  devices = []
  sql = 'SELECT * FROM device ORDER by name'
  cur.execute(sql)
  conn.commit()
  devices = cur.fetchall()
  return devices

def getAllActiveDevices(conn,cur):
  devices = []
  sql = "SELECT * FROM device WHERE active='t' ORDER by name"
  cur.execute(sql)
  conn.commit()
  devices = cur.fetchall()
  return devices

def getAllDevicesHtml(conn,cur):
  html = ''''<script>
    function showFPImage(id){
      var iframe = document.getElementById('deviceFPImageFrame');
      iframe.src = "index.py?showFPDeviceId="+id;
      iframe.style.display = "block";
      var button = document.getElementById('buttonCloseFPImage');
      button.style.display = "block";
    }
    function closeFPImage(){
      var iframe = document.getElementById('deviceFPImageFrame');
      iframe.src = "";
      iframe.style.display = "none";
      var button = document.getElementById('buttonCloseFPImage');
      button.style.display = "none";
    }
  </script>
'''
  html += '<iframe id="deviceFPImageFrame" src="" style="display:none;position:absolute;width:100%;height:100%;background-color:rgba(0, 0, 0, 0.8);"></iframe><input type="button" id="buttonCloseFPImage" value="Close" style="position:fixed;top:130px;left:10px;display:none;" onclick="closeFPImage()">'
  html += '<table class="reference notranslate"><tr><th>Name</th><th>Active</th><th>Mute<br>notifications</th><th>Floorplan map</th><th>Temperature<br>1&deg; threshold </th><th>Temperature<br>2&deg; threshold</th><th>Humidity<br>1&deg; threshold</th><th>Humidity<br>2&deg; threshold</th><th>Action</th></tr><br>'
  html += '<tr><form id="addDevice" method="post" enctype="multipart/form-data"><td><input type="text" name="deviceName" required></td><td><input type="checkbox" name="deviceActive" checked></td><td><input type="checkbox" name="deviceMuteNoti"></td><td><input type="file" name="deviceFP" accept=".png"></td><td><input type="number" name="tempWarning" value="32.0" step="0.1" min="16.0" max="60.0" style="width:50px">&#176;C</td><td><input type="number" name="tempCritical" value="35.0" step="0.1" min="16.0" max="60.0" style="width:50px">&#176;C</td><td><input type="number" name="humidityWarning" value="70.0" step="0.1" min="0.0" max="100.0" style="width:50px">&#37;</td><td><input type="number" name="humidityCritical" value="80.0" step="0.1" min="0.0" max="100.0" style="width:50px">&#37;</td><td><input type="submit" name="addDevice" value="Add device"></td></form></tr>'
  devs = getAllDevices(conn,cur)
  for dev in devs:
    html += '<tr><form id="delDevice" method="post" enctype="multipart/form-data"><td>'+dev['name']+'<input type="hidden" name="devId" value="'+str(dev['id'])+'"></td><td><input type="checkbox" name="deviceActive" '
    if dev['active']:
      html += 'checked'
    html += '></td><td><input type="checkbox" name="deviceMuteNoti" '
    if dev['mutealarmsnotif']:
      html += 'checked'
    html += '></td><td><input type="button" value="Show current" onclick="showFPImage(\''+str(dev['id'])+'\')"><br><input type="file" name="deviceFP" ></td><td><input type="number" name="tempWarning" value="'+str(dev['tempreaturewarning']/10.0)+'" style="width:50px" step="0.1" min="16.0" max="60.0">&#176;C</td><td><input type="number" name="tempCritical" value="'+str(dev['tempreaturecritical']/10.0)+'" style="width:50px" step="0.1" min="16.0" max="60.0">&#176;C</td><td><input type="number" name="humidityWarning" value="'+str(dev['humiditywarning']/10.0)+'" style="width:50px" step="0.1" min="0.0" max="100.0">&#37;</td><td><input type="number" name="humidityCritical" value="'+str(dev['humiditycritical']/10.0)+'" style="width:50px" step="0.1" min="0.0" max="100.0">&#37;</td><td><input type="submit" name="modDevice" value="Save changes"><br><input type="submit" name="rmvDevice" value="Remove device" '
    if dev['active']:
      html += 'disabled'
    html += '></td>'
    html += '</form></tr>'
  html += '</table>'
  return html
