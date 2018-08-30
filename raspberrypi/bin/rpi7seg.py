#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import sys

def printDisp(n, d):
  if n==0:
    GPIO.setup(d[0], GPIO.OUT)
    GPIO.output(d[0], 0)
    GPIO.setup(d[1], GPIO.IN)
    GPIO.setup(d[2], GPIO.IN)
  elif n==1:
    GPIO.setup(d[0], GPIO.IN)
    GPIO.setup(d[1], GPIO.OUT)
    GPIO.output(d[1], 0)
    GPIO.setup(d[2], GPIO.IN)
  elif n==2:
    GPIO.setup(d[0], GPIO.IN)
    GPIO.setup(d[1], GPIO.IN)
    GPIO.setup(d[2], GPIO.OUT)
    GPIO.output(d[2], 0)

def cleanAllDisp(d):
    GPIO.setup(d[0], GPIO.IN)
    GPIO.setup(d[1], GPIO.IN)
    GPIO.setup(d[2], GPIO.IN)

def print7S(n, W):
  if n==0:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 0)
  elif n==1:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 0)
  elif n==2:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 0)
  elif n==3:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 0)
  elif n==4:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 0)
  elif n==5:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 0)
  elif n==6:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 0)
  elif n==7:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 0)
  elif n==8:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 1)
  elif n==9:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 1)
  elif n==10:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 1)
  elif n==11:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 0)
    GPIO.output(W[3], 1)
  elif n==12:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 1)
  elif n==13:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 0)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 1)
  elif n==14:
    GPIO.output(W[0], 0)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 1)
  elif n==15:
    GPIO.output(W[0], 1)
    GPIO.output(W[1], 1)
    GPIO.output(W[2], 1)
    GPIO.output(W[3], 1)

w=sys.argv[1]
t=int(sys.argv[2])
pc={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'c':10,'t':14,' ':15}

W = (10,16,18,8)
d = (15,11,12)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(W[0], GPIO.OUT)
GPIO.setup(W[1], GPIO.OUT)
GPIO.setup(W[2], GPIO.OUT)
GPIO.setup(W[3], GPIO.OUT)

t1=time.time()
t2=t1
while not (t2-t1)>t:
  for j in range(0,3):
    cleanAllDisp(d)
    print7S(pc[w[j]],W)
    printDisp(j,d)
    time.sleep(0.006)
  t2=time.time()

#for iw in w:
#  print iw
#  if iw in pc:
#    print7S(pc[iw],W)
#    time.sleep(1)

#for x in range(0,3):
#  printDisp(x,d)
#  for i in range(0,16):
#    print7S(i,W)
#    time.sleep(0.5)
#time.sleep(10)
GPIO.cleanup()
quit(0)
