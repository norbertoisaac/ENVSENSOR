#! /usr/bin/python
import psycopg2
import sys
import os
def getDbConn():
  try:
    conn = psycopg2.connect('dbname=sensor user=agent password=/74gnR%%R host=10.140.71.99 connect_timeout=3')
    cur = conn.cursor()
    return conn,cur
  except Exception as e:
    return None,e
  else:
    return None,None

inres = 0
if 'SCRIPT_FILENAME' in os.environ:
  pass
