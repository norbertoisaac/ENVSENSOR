#! /usr/bin/python
import psycopg2
import psycopg2.extras
import sys
import os
inres = 0
homeDir='/var/lib/radmin'
imagesDB=homeDir+'/files/images'
if 'SCRIPT_FILENAME' in os.environ:
  if '/dbconn.py' in os.environ['SCRIPT_FILENAME']:
    inres = 1
    body = ''
    headers = 'Content-Type: text/plain; charset=utf-8\r\n'
    headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
    sys.stdout.write(headers+body)
  else:
    conn = psycopg2.connect('dbname=envsensor user=envsysfe password=%envT434% host=127.0.0.1')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
else:
  quit()
