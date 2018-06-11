#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import socket
import pickle
import json
# web server when receive the results of dog pose
def main():
  s = socket.socket()
  host = 'localhost'
  port = 12342
  s.connect((host, port))
  client_data = s.recv(1024)
  try:
    pickle_data = pickle.loads(client_data)
    pickle_data['predictions'] = str(pickle_data['predictions'])
    jason = json.dumps(pickle_data)
    print()
    print(jason)

  except EOFError:
    print('eoferror')
  s.close()
if __name__ == '__main__':
  main()

