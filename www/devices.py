def addDevice(dev):
  sql = 'INSERT INTO device(name,active,tempreatureWarning,tempreatureCritical,humidityWarning,humidityCritical) VALUES ()'
  return

def getAllDevices(conn,cur):
  devices = []
  sql = 'SELECT * FROM device ORDER by name'
  cur.execute(sql)
  conn.commit()
  devices = cur.fetchall()
  return devices

def getAllDevicesHtml(conn,cur):
  html = '<table class="reference notranslate"><tr><th>Name</th><th>Active</th><th>Mute<br>notifications</th><th>Temperature<br>warning<br>threshold</th><th>Temperature<br>critical<br>threshold</th><th>Humidity<br>warning<br>threshold</th><th>Humidity<br>critical<br>threshold</th><th>Action</th></tr><br>'
  html += '<tr><form id="addDevice" method="post"><td><input type="text" name="deviceName"></td><td><input type="checkbox" name="deviceActive" checked></td><td><input type="checkbox" name="deviceMuteNoti"></td><td><input type="number" name="tempWarning" value="32.0" step="0.1"></td><td><input type="number" name="tempCritical" value="35.0" step="0.1"></td><td><input type="number" name="humidityWarning" value="70.0" step="0.1"></td><td><input type="number" name="humidityCritical" value="80.0" step="0.1"></td><td><input type="submit" name="addDevice" value="Add device"></td></form></tr>'
  devs = getAllDevices(conn,cur)
  for dev in devs:
    html += '<tr><td>'+dev['name']+'</td></tr>'
  html += '</table>'
  return html
