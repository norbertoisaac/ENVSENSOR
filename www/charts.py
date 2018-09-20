import devices
def getAllCharts(conn,cur):
  import graph
  import base64
  body = ''
  devs = devices.getAllActiveDevices(conn,cur)
  for dev in devs:
    graph.graph_draw(conn,cur,dev['name'])
    body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  return body
