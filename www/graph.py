# -*- coding: utf-8 -*-
import tempfile
import os
import sys
from pychart import *
#theme.output_format = 'svg'
#theme.default_font_size = 5
theme.use_color = True
#theme.delta_bounding_box = (0,0,5,-10)
#theme.default_line_height = 1
theme.reinitialize()
body = ''
altura = 250
alturaAcum = 0

def graph_format(formato):
  theme.output_format = formato
  theme.reinitialize()

def format_data_label(x,y):
  global body
  res = ''
  #if x.minute%10 == 0 :
  if x.minute == 0 and (x.hour%3)==0:
    res = '/C/15/a90{}'+str(y)
    #body += str(y)
    #sys.stdout.write(str(y))
  return res

def format_tic_interval24(tst):
 return format_tic_interval(tst,'24h')

def format_tic_interval12h(tst):
 return format_tic_interval(tst,'12h')

def format_tic_interval6h(tst):
 return format_tic_interval(tst,'6h')

def format_tic_interval1h(tst):
 return format_tic_interval(tst,'1h')

def format_tic_interval(tst,lapso=None):
  global body
  tstList = []
  if lapso==None or lapso=='24h':
    if tst.minute==0 and tst.hour==0:
      tst = "/a90{}"+tst.strftime('%Y-%m-%d')+' '
    elif (tst.hour%2)==0 and tst.minute==0:
      tst = "/a90{}"+str(tst.hour)+' : '+str(tst.minute).zfill(2)+' '
    else:
      tst = ''
  elif lapso=='12h':
    if tst.minute==0:
      tst = "/a90{}"+str(tst.hour)+' : '+str(tst.minute).zfill(2)+' '
    else:
      tst = ''
  elif lapso=='6h':
    if (tst.minute%30)==0:
      tst = "/a90{}"+str(tst.hour)+' : '+str(tst.minute).zfill(2)+' '
    else:
      tst = ''
  elif lapso=='1h':
    if tst.minute==0:
      tst = "/a90{}"+str(tst.hour)+' : '+str(tst.minute).zfill(2)+' '
    elif (tst.minute%5)==0:
      tst = "/a90{}"+str(tst.minute).zfill(2)+' '
    else:
      tst = ''
  else:
    tst = ''
  return tst

def graphconf(conn,cur,sonda,lapso=None):
  table='temp_and_humd_log'
  condicion='status=0 and name=\''+sonda+'\''
  tic_interval = format_tic_interval24
  if lapso=='1h':
    tic_interval = format_tic_interval1h
    interval=("(CURRENT_TIMESTAMP - interval '1 hours')","CURRENT_TIMESTAMP")
  elif lapso=='6h':
    tic_interval = format_tic_interval6h
    interval=("(CURRENT_TIMESTAMP - interval '6 hours')","CURRENT_TIMESTAMP")
  elif lapso=='12h':
    tic_interval = format_tic_interval12h
    interval=("(CURRENT_TIMESTAMP - interval '12 hours')","CURRENT_TIMESTAMP")
  elif lapso=='Ayer':
    tic_interval = format_tic_interval24
    interval=("date_trunc('day',CURRENT_TIMESTAMP - interval '24 hours')","date_trunc('day',CURRENT_TIMESTAMP)")
  elif lapso=='7d':
    table='temp_and_humd_hist'
    condicion='(temperature<700 AND name=\''+sonda+'\')'
    interval=("date_trunc('day',CURRENT_TIMESTAMP - interval '8 days')","date_trunc('day',CURRENT_TIMESTAMP-interval '24 hours')")
  elif lapso=='30d':
    table='temp_and_humd_hist'
    condicion='(temperature<700 AND name=\''+sonda+'\')'
    interval=("date_trunc('day',CURRENT_TIMESTAMP - interval '30 days')","date_trunc('day',CURRENT_TIMESTAMP-interval '24 hours')")
  else:
    tic_interval = format_tic_interval24
    interval=("(CURRENT_TIMESTAMP - interval '24 hours')","CURRENT_TIMESTAMP")
  sql = "WITH sel1 AS (SELECT date_trunc('min',sampletime)::timestamp AS tst, temperature/10.0 AS t, humidity/10.0 AS h FROM "+table+" WHERE sampletime > "+interval[0]+" AND sampletime <= "+interval[1]+" AND "+condicion+" ORDER BY tst ASC) SELECT tst,round(avg(t),1)::real AS tp,round(avg(h),1)::real AS hm FROM sel1 GROUP BY tst ORDER BY tst;"
  cur.execute(sql)
  conn.commit()
  data = cur.fetchall()
  graph_draw(data,sonda,tic_interval) 
  return

def graph_draw(temperatureData,name,tic_interval):
  global body
  global alturaAcum
  body = ''
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format='png')
  #can = canvas.init(fname,format='svg')

  # grafico de la temperatura
  #sql = "SELECT date_trunc('min',sampletime) as tst,avg(temperature/10) FROM temp_and_humd_log WHERE sampletime > (CURRENT_TIMESTAMP - interval '24 hours') AND status=0 ORDER BY sampletime ASC GROUP BY tst"
  if len(temperatureData) == 0:
    import datetime
    temperatureData = ((datetime.datetime.today(),0,0),)
  maxS = ('',0,0)
  for t in temperatureData:
    #body += str(t)
    if t[1] > maxS[1]:
      maxS = t
  last = temperatureData[-1]
  #"+str(maxS[0].hour)+":"+str(maxS[0].minute)+"
  lastText = "/H/85{}"+str(last[1])+"°\n/15{} Humedad: "+str(last[2])+"% a las "+str(last[0].hour)+":"+str(last[0].minute)+"\n/15{} Max. "+str(maxS[1])+"° fecha "+str(maxS[0].day)+' a las '+str(maxS[0].hour).zfill(2)+":"+str(maxS[0].minute).zfill(2)
  #tb = text_box.T(loc=(0,-245), text=lastText.decode('utf8'), fill_style=None, top_fudge=1, bottom_fudge=1, right_fudge=1, left_fudge=1, shadow=None)
  tb = text_box.T(loc=(90,5), text=lastText.decode('utf8'), fill_style=None, top_fudge=1, bottom_fudge=1, right_fudge=1, left_fudge=1, shadow=None)
  tb.draw()
  #can.show(160, 140, "/10 Temperatura en Sala1")
  can.show(5, 250, "/45/H"+str(name))
  #lastText = "/185{}"+str(last[1])+"°"
  #can.show(430,10,lastText.decode('utf8'))
  #can.show(73, 50, "Temperatura en Sala1")
  l = legend.T(loc=(54,-50),nr_rows=1)
  #l = legend.T(nr_rows=1)
  ar = area.T(legend = l,
              #bg_style = fill_style.yellow,
	      #loc=(0,alturaAcum),
	      #size = (450,143),
	      size = (300,243),
              #size = None,
	      x_coord = category_coord.T(temperatureData, 0),
	      #y_coord = linear_coord.T(temperatureData, 2),
	      y_range = (0, maxS[1]+10.0),
	      y_grid_interval =5,
	      #x_axis = axis.X(label_offset = (170,50), format = format_tic_interval, tic_len=0),
	      x_axis = axis.X(label = "", label_offset = (170,50), format = tic_interval, tic_len=0),
	      #x_axis = axis.X(label = "Date", format = "/a90{}%s"),
	      #y_axis = axis.Y(label = "SMS enviados", format="%d", tic_interval = 200))
	      #y_axis = axis.Y(label = "Temperatura °C", format="%d", tic_interval = maximo/10))
	      #y_axis = axis.Y(label = "Temperatura °C".decode('utf8'), tic_interval = 2, format = "%f"))
	      y_axis = axis.Y(label="".decode('utf8'),tic_interval = 5))
  #plot1 = bar_plot.T(data = temperatureData, line_style=None, fill_style=fill_style.green, label="Sala 1".decode('utf8'), data_label_format = format_data_label, data_label_offset = (0,3))
  plot1 = line_plot.T(data = temperatureData, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Temperatura °C".decode('utf8'), data_label_format = format_data_label, data_label_offset = (0,3))
  plot2 = line_plot.T(data = temperatureData, ycol=2, line_style = line_style.T(color=color.blue,width=4.0), label=" /15Humedad %".decode('utf8'), data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1,plot2)
  try:
    ar.draw(can)
  except UnicodeDecodeError as e:
    body += str(e)
  except TypeError as e:
    body += str(e)
  except AttributeError as e:
    body += str(e)
  #lastText = "/15Actual: Tiempo= "+str(last[0].hour)+":"+str(last[0].minute)+", Temperatura= "+str(last[1])+" °C, Humedad= "+str(last[2])+" %"
  #tb = text_box.T(loc=(150,-85), text=lastText.decode('utf8'))
  #tb.draw()
  # DISPLAY

  try:
    can.close()
  except AttributeError as e:
    body += str(e)
  lenOfF = os.path.getsize(fname)
  os.lseek(f,0,os.SEEK_SET)
  body += os.read(f,lenOfF)

  os.close(f)
  os.unlink(fname)
