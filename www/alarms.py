def getAlarmLog(conn,cur,active,cleared,ack,devId,count):
  alarms = []
  return alarms

def getAlarmLogHtml(conn,cur,active,cleared,ack,devId,count):
  html = ''
  alarms = getAlarmLog(conn,cur,active,cleared,ack,devId,count)
  return html
