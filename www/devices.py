def addDevice(dev,conn,cur):
  sql = "INSERT INTO device(name,active,muteAlarmsNotif,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) VALUES (%(name)s,%(active)s,%(muteNoti)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s)"
  cur.execute(sql,dev)
  conn.commit()
  return

def modDevice(dev,conn,cur):
  sql = "UPDATE device SET (active,muteAlarmsNotif,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) = (%(active)s,%(muteNoti)s,%(twt)s,%(tct)s,%(hwt)s,%(hct)s) WHERE id=%(id)s"
  cur.execute(sql,dev)
  conn.commit()
  return

def getAllDevices(conn,cur):
  devices = []
  sql = 'SELECT * FROM device ORDER by name'
  cur.execute(sql)
  conn.commit()
  devices = cur.fetchall()
  return devices

def getAllDevicesHtml(conn,cur):
  html = '<table class="reference notranslate"><tr><th>Name</th><th>Active</th><th>Mute<br>notifications</th><th>Floorplan map</th><th>Temperature<br>warning<br>threshold &#176;C</th><th>Temperature<br>critical<br>threshold &#176;C</th><th>Humidity<br>warning<br>threshold &#37;</th><th>Humidity<br>critical<br>threshold &#37;</th><th>Action</th></tr><br>'
  html += '<tr><form id="addDevice" method="post" enctype="multipart/form-data"><td><input type="text" name="deviceName" required></td><td><input type="checkbox" name="deviceActive" checked></td><td><input type="checkbox" name="deviceMuteNoti"></td><td><input type="file" name="deviceFP" accept=".png"></td><td><input type="number" name="tempWarning" value="32.0" step="0.1" style="width:50px"></td><td><input type="number" name="tempCritical" value="35.0" step="0.1" style="width:50px"></td><td><input type="number" name="humidityWarning" value="70.0" step="0.1" style="width:50px"></td><td><input type="number" name="humidityCritical" value="80.0" step="0.1" style="width:50px"></td><td><input type="submit" name="addDevice" value="Add device"></td></form></tr>'
  devs = getAllDevices(conn,cur)
  for dev in devs:
    html += '<tr><form id="delDevice" method="post" enctype="multipart/form-data"><td>'+dev['name']+'<input type="hidden" name="devId" value="'+str(dev['id'])+'"></td><td><input type="checkbox" name="deviceActive" '
    if dev['active']:
      html += 'checked'
    html += '></td><td><input type="checkbox" name="deviceMuteNoti" '
    if dev['mutealarmsnotif']:
      html += 'checked'
    html += '></td><td><input type="file" name="deviceFP"></td><td><input type="number" name="tempWarning" value="'+str(dev['tempreaturewarning']/10.0)+'" style="width:50px" step="0.1"></td><td><input type="number" name="tempCritical" value="'+str(dev['tempreaturecritical']/10.0)+'" style="width:50px" step="0.1"></td><td><input type="number" name="humidityWarning" value="'+str(dev['humiditywarning']/10.0)+'" style="width:50px" step="0.1"></td><td><input type="number" name="humidityCritical" value="'+str(dev['humiditycritical']/10.0)+'" style="width:50px" step="0.1"></td><td><input type="submit" name="modDevice" value="Save changes"><br><input type="submit" name="rmvDevice" value="Remove device"></td>'
    html += '</form></tr>'
  html += '</table>'
  return html
