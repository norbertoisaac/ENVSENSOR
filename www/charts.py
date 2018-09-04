def getAllCharts(conn,cur):
  import graph
  import base64
  body = ''
  graph.graph_draw(conn,cur,'MSCFDO-Sala2')
  body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  graph.graph_draw(conn,cur,'MSCFDO-Sala1')
  body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  graph.graph_draw(conn,cur,'MSCCDE-Sala1')
  body+= '<img src="data:image/png;base64,'+base64.b64encode(graph.body)+'" />'
  return body
