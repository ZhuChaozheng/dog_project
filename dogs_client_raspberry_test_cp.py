#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 引入必要的module
import serial
import socket
import pickle
import time

def main():
  r = []
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
  s.close()


if __name__ == "__main__":
    while 1:
        main()
