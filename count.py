#!/usr/bin/python3
import os
import socket
import pickle
# web server when receive the results of dog pose
def main():
  s = socket.socket()
  host = 'localhost'
  port = 12341
  s.connect((host, port))
  print('22')
  client_data = s.recv(1024)
  try:
    pickle_data = pickle.loads(client_data)
    print(pickle_data)
  except EOFError:
    print('eoferror')
  s.close()
if __name__ == '__main__':
  main()

