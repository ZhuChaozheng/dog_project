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
  host = 'server.blackant.org'
#  host = '180.109.138.23'
#   host = '127.0.0.1'
  port = 10011
  try:
    s.connect((host, port))
    print('connected')
  except:
      print('request refused')
  # demo data
#  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c',
#  '01', '1e', '6c', '01', '1e', '6c', '00', '3e', '6c', '00', '7e', '0c']
  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c']
  flag = 0
  while True:
        #print('ii', r)
        if (flag == 0):
            r = ['00', '16', '61', '01', 'ea', '41', '00', 'e0', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c']
            flag = 1
            print('0')
        else:
            flag = 0
            r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c', '00', 'e0', '6c', '6c', '01', 'ea', '00', 'e0', '6c', '6c', '01', 'ea', 'aa', 'aa']
            print('1')
#        a = json.dumps(r).encode('utf-8')
        r.append('p002')
        a = pickle.dumps(r)
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
