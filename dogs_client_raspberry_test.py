#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 引入必要的module
import serial
import socket
import pickle
import time
import json

def main():
  r = []
  s = socket.socket()

  # host = 'server.blackant.org'
#  host = 'server.blackant.org'
#  host = '180.109.138.23'
  host = '127.0.0.1'
  port = 12343
  try:
    s.connect((host, port))
    print('connected')
  except:
      print('request refused')
  # demo data
#  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c',
#  '01', '1e', '6c', '01', '1e', '6c', '00', '3e', '6c', '00', '7e', '0c']
  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c']
  while True:
        #print('ii', r)
        a = json.dumps(r).encode('utf-8')
        try:
            s.send(a)
        except:
            print('connect break')
            s.close()
            break
        time.sleep(1)    
  s.close()


if __name__ == "__main__":
    while 1:
        main()
