#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 引入必要的module
import serial
import socket
import pickle
import time

def main():
  # read serial
#  x = serial.Serial('/dev/ttyUSB0', 115200)
  r = []
  num = 0
  num1 = 0
  length = 0
  j = 0
  s = socket.socket()
  host = 'server.blackant.org'
#  host = '180.109.138.23'
  port = 12343
  s.connect((host, port))
  # demo data
  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c',
  '01', '1e', '6c', '01', '1e', '6c', '00', '3e', '6c', '00', '7e', '0c']
  while True:
        #print('ii', r)
        a = pickle.dumps(r)
        s.send(a)
        time.sleep(1)
    # if num == 26:
    #    num = 0
    #    num1 = 0
    #    r = []
  s.close()

if __name__ == "__main__":
    main()
