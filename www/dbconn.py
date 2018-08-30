#! /usr/bin/python
import psycopg2
import sys
import os
inres = 0
if 'SCRIPT_FILENAME' in os.environ:
  if os.environ['SCRIPT_FILENAME'] == '/var/www/html/cgi-script/sensor/dbconn.py':
    inres = 1
    body = ''
    headers = 'Content-Type: text/plain; charset=utf-8\r\n'
    headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
    sys.stdout.write(headers+body)
  else:
    conn = psycopg2.connect('dbname=sensor user=agent password=%Rn/74gR% host=10.150.31.69')
    cur = conn.cursor()
else:
  quit()
