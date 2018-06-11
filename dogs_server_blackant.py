#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 引入必要的module
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pickle
import time
import os
import math
import urllib
import serial
import socket
import threading

flag = 0
all_sensors_data = {'yaw_one':0, 'pitch_one':2.3, 'roll_one':0, 'yaw_two':0, 'pitch_two':2.91, 'roll_two':0, 'ridar':0, 'predictions':2}
threadLock = threading.Lock()
sensors_data = {'yaw_one':0, 'pitch_one':0, 'roll_one':0, 'yaw_two':0, 'pitch_two':0, 'roll_two':0, 'ridar':0, 'predictions':0}
web_sensors_data = {'yaw_one':0, 'pitch_one':0, 'roll_one':0, 'yaw_two':0, 'pitch_two':0, 'roll_two':0, 'ridar':0, 'predictions':0}
num = 0  # valid data sets number
current_sensor_data = [0, 0, 0]
last_sensor_data = [0, 0, 0]
predictions_data = 0

# this method is used to obtain type int data for each data
def slice_data(r):
  global all_sensors_data
  sensor_data = []
  if len(r) < 10:
    return [0, 0, 0, 0, 0, 0, 0, 0, 0]
  yaw_str_one = ''.join(r[0:2])
  yaw_int_one = int(yaw_str_one, 16)
  yaw_one_sign = int(r[2], 16)
  if yaw_one_sign == 0:
    yaw_int_one = yaw_int_one
  else:
    yaw_int_one = -yaw_int_one
  yaw_int_one = yaw_int_one / 100
#  sensor_data.append(yaw_int_one)
  sensors_data['yaw_one'] = yaw_int_one

  pitch_str_one = ''.join(r[3:5])
  pitch_int_one = int(pitch_str_one, 16)
  pitch_one_sign = int(r[5], 16)
  if pitch_one_sign == 0:
    pitch_int_one = pitch_int_one
  else:
    pitch_int_one = -pitch_int_one
  pitch_int_one = pitch_int_one / 100
  sensor_data.append(pitch_int_one)
  sensors_data['pitch_one'] = pitch_int_one

  roll_str_one = ''.join(r[6:8])
  roll_int_one = int(roll_str_one, 16)
  roll_one_sign = int(r[8], 16)
  if roll_one_sign == 0:
    roll_int_one = roll_int_one
  else:
    roll_int_one = -roll_int_one
  roll_int_one = roll_int_one / 100
  sensors_data['roll_one'] = roll_int_one

  yaw_str_two = ''.join(r[9:11])
  yaw_int_two = int(yaw_str_two, 16)
  yaw_two_sign = int(r[11], 16)
  if yaw_two_sign == 0:
    yaw_int_two = yaw_int_two
  else:
    yaw_int_two = -yaw_int_two
  yaw_int_two = yaw_int_two / 100
 # sensor_data.append(yaw_int_two)
  sensors_data['yaw_two'] = yaw_int_two

  pitch_str_two = ''.join(r[12:14])
  pitch_int_two = int(pitch_str_two, 16)
  pitch_two_sign = int(r[14], 16)
  if pitch_two_sign == 0:
    pitch_int_two = pitch_int_two
  else:
    pitch_int_two = -pitch_int_two
  pitch_int_two = pitch_int_two / 100
  sensor_data.append(pitch_int_two)
  sensors_data['pitch_two'] = pitch_int_two

  roll_str_two = ''.join(r[15:17])
  roll_int_two = int(roll_str_two, 16)
  roll_int_sign = int(r[17], 16)
  if roll_int_sign == 0:
    roll_int_two = roll_int_two
  else:
    roll_int_two = -roll_int_two
  roll_int_two = roll_int_two / 100
  sensors_data['roll_two'] = roll_int_two

  ridar_str = ''.join(r[18:20])
  ridar_int = int(ridar_str, 16)
  ridar_int_sign = int(r[20], 16)
  if ridar_int_sign == 0:
    ridar_int = ridar_int
  else:
    ridar_int = -ridar_int
  print('ridar', ridar_int)
  sensor_data.append(ridar_int)
  sensors_data['ridar'] = ridar_int
  threadLock.acquire()
  all_sensors_data = sensors_data.copy()
  #print(all_sensors_data)
  threadLock.release()
  print('sensor_data', sensor_data)
  return sensor_data



# angle1 is 0~180, -180~-0, angle2 is 0~180, -180~-0
def offset_angle(angle1, angle2):
  if (math.fabs(angle1 - angle2) > 180):
    angle = 360 - (math.fabs(angle1) + math.fabs(angle2))
  else:
    angle = math.fabs(angle1) - math.fabs(angle2)
  return angle


# Data validation: floating between two sets of data does not exceed 10%, if it is right, return true, else return false
def data_validation(sensor_data):
  #print('data_validation', sensor_data)
  global current_sensor_data
  global last_sensor_data
  current_sensor_data = sensor_data
  #print('last_sensor_data', last_sensor_data)
  #print('current_sensor_data', current_sensor_data)
  # assign an initial value to last_sensor_data, when it is the first
  if (last_sensor_data[0] == 0 and last_sensor_data[1] == 0 and last_sensor_data[2] == 0):
    last_sensor_data = current_sensor_data
    return False
  # validate data in the range of 10%
  print(offset_angle(last_sensor_data[0], current_sensor_data[0]))
  if (offset_angle(last_sensor_data[0], current_sensor_data[0]) > 10):
    print('error 1')
    last_sensor_data = current_sensor_data
    return False
  if (offset_angle(last_sensor_data[1], current_sensor_data[1]) > 10):
    print('error 2')
    last_sensor_data = current_sensor_data
    return False
    # height need particularly handle, as its range isn't 0~180,-0~-180
  if (math.fabs(last_sensor_data[2]) - 30 > math.fabs(current_sensor_data[2]) or math.fabs(current_sensor_data[2]) > math.fabs(last_sensor_data[2]) + 30):
    print('error 3')
    last_sensor_data = current_sensor_data
    return False
  print('data_validation true')
  return True

# initial system, command dog to stand up until it return 10 sets valid data
def initial_system(sensor_data):
  print('initial', sensor_data)
  global num
  if (data_validation(sensor_data)):
    num = num + 1
  else:
    num = 0
  # finish initial system, predictions is 3, or predictions is 4
  global predictions_data
  print('num', num)
  if (num > 5):
    predictions_data = 3
    return True
  else:
    predictions_data = 4
    return False

def predictions_decision_tree(sensor_data):
  print('decision', sensor_data)
  print('current', current_sensor_data)  # precise data for dog stand up, after intial, it will not be updated
  global all_sensors_data
  global web_sensors_data
  global predictions_data
  global flag
#  print(sensor_data)
#  print(flag)
  if (flag == 0):
    if (initial_system(sensor_data)):
      flag = 1
      print('initial finished')
  else:
      # height need particularly handle, as its range isn't 0~180,-0~-180
    if ((math.fabs(sensor_data[2]) < math.fabs(current_sensor_data[2]) - 100) and (offset_angle(sensor_data[0], current_sensor_data[0]) < 10 or (offset_angle(sensor_data[1], current_sensor_data[1]) < 10))):
# lay
      predictions_data = 0
    if ((offset_angle(sensor_data[0], current_sensor_data[0]) > 20) or (offset_angle(sensor_data[0], current_sensor_data[0]) > 20)):
# down
      predictions_data = 2
    if ((offset_angle(sensor_data[0], current_sensor_data[0]) < 20) or (offset_angle(sensor_data[0], current_sensor_data[0]) < 20)):
# up
      predictions_data = 1

    threadLock.acquire()
    all_sensors_data['predictions'] = predictions_data
    threadLock.release()
    web_sensors_data = all_sensors_data.copy()
    #print(web_sensors_data)
    return

  threadLock.acquire()
  all_sensors_data['predictions'] = predictions_data
  threadLock.release()
  web_sensors_data = all_sensors_data.copy()


def web_server(threadName, delay):
  # client server
  server = socket.socket()
  host_server = '0.0.0.0'
  port_server = 12342
  server.bind((host_server, port_server))
  server.listen(5)
#  predictions = [1]
#  global web_isensors_data
  while True:
    c, addr = server.accept()
    print('web', addr)
    try:
#      print('web', web_sensors_data)
      print('web', predictions_data)
      a = pickle.dumps(web_sensors_data)
      c.send(a)
      c.close()
    except EOFError:
      print('eoferror')
  #    flag = 0
  server.close()


def tcp_server(threadName, delay):
#  print('tcp')
  s = socket.socket()
  host = '0.0.0.0'
  port = 12343
  s.bind((host,port))
  s.listen(5)
  # start dnn
#  global all_sensors_data
#  all_sensors_data = {'yaw_one':0, 'pitch_one':0, 'roll_one':0, 'yaw_two':0, 'pitch_two':0, 'roll_two':0, 'ridar':0, 'predictions':0}
#  predictions_motion()
  while True:
      c, addr = s.accept()
      print ('111',addr)
      while True:
          client_data = c.recv(1024)
          if not client_data:
              print('disconnect')
              break
#          print(client_data)
#          pickle_data = client_data.split('.')
          try:
            pickle_data = pickle.loads(client_data)
          except EOFError:
            print('pickle.loads error')
  #        print('server ', pickle_data)
          sensor_data = slice_data(pickle_data)
  #        print('slice_data', sensor_data)
      #    while True:
      #      if flag == 0:
      #        print('flag_tcp', flag)
      ##    predictions_motion()
          predictions_decision_tree(sensor_data)
         # print(all_sensors_data)
      #        flag = 1
      #        break
      c.close()
# as a tcp server receive the data of dog police pose, also as a web client, send the results of pose
def main():

  try:
    t1 = threading.Thread(target=web_server, args=('Thread-1', 2, ))
    t2 = threading.Thread(target=tcp_server, args=('Thread-2', 3, ))
    t1.start()
    t2.start()
  except:
    print('Error: unable to start thread')
  while 1:
    pass
if __name__ == "__main__":
    main()
