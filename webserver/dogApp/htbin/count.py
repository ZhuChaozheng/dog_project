#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import socket
import pickle
import json
# web server when receive the results of dog pose


def main(num):
  s = socket.socket()
  host = 'localhost'
  # host = 'server.blackant.org'
  port = 10010
  s.connect((host, port))
  client_data = s.recv(1024)
  try:
    pickle_data = pickle.loads(client_data)
    # print(pickle_data)
  
    if pickle_data['dog_name'] == num:
      pickle_data['predictions'] = str(pickle_data['predictions'])
      jason = pickle_data
      # print ("Content-type: application/json")
      s.close()
      # print(jason)
      return jason
        
  except EOFError:
    print('eoferror')
    s.close()
  
  
# if __name__ == '__main__':
#   main()


