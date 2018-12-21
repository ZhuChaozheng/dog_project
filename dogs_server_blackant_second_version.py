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
import pymysql
import datetime

flag = 0  # for initial system
flag_database = 0  # for database thread
all_sensors_data = {'yaw_one': 0, 'pitch_one': 2.3, 'roll_one': 0, 'yaw_two': 0, 'pitch_two': 2.91, 'roll_two': 0, 'height': 0, 'predictions': 2}
threadLock = threading.Lock()
sensors_data = {'yaw_one': 0, 'pitch_one': 0, 'roll_one': 0, 'yaw_two': 0, 'pitch_two': 0, 'roll_two': 0, 'height': 0, 'predictions': 0}
# contrast with twice web_sensors_data
web_sensors_data = {'yaw_one': 0, 'pitch_one': 0, 'roll_one': 0, 'yaw_two': 0, 'pitch_two': 0, 'roll_two': 0, 'height': 0, 'predictions': 0}
last_web_sensors_data = {'yaw_one': 0, 'pitch_one': 0, 'roll_one': 0, 'yaw_two': 0, 'pitch_two': 0, 'roll_two': 0, 'height': 0, 'predictions': 0}

num = 0  # valid data sets number
# contrast with twice sensor_data [pitch_one, pitch_two, height]
current_sensor_data = [0, 0, 0]
last_sensor_data = [0, 0, 0]

# set predictions_data = 5, represent disconnect
predictions_data = 5

# need a global variable to add a new feature run
velocity = 0

# cmp comprise two dict
def cmp_dict(src_data, dst_data):
    sum_v_d = 0
    sum_v_d1 = 0
    for value in src_data.values():
        sum_v_d = value + sum_v_d
    for value in dst_data.values():
        sum_v_d1 = value + sum_v_d1
    if (sum_v_d == sum_v_d1):
        return 0
    return 1


# this method is used to obtain type int data for each data
def slice_data(r):
    global velocity
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
    velocity = yaw_int_one
    print(velocity)

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
    print(pitch_int_one)

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
    print(pitch_int_two)

    roll_str_two = ''.join(r[15:17])
    roll_int_two = int(roll_str_two, 16)
    roll_int_sign = int(r[17], 16)
    if roll_int_sign == 0:
        roll_int_two = roll_int_two
    else:
        roll_int_two = -roll_int_two
    roll_int_two = roll_int_two / 100
    sensors_data['roll_two'] = roll_int_two

    height_str = ''.join(r[18:20])
    height_int = int(height_str, 16)
    height_int_sign = int(r[20], 16)
    if height_int_sign == 0:
        height_int = height_int
    else:
        height_int = -height_int
    print('height', height_int)
    sensor_data.append(height_int)
    sensors_data['height'] = height_int

    threadLock.acquire()
    all_sensors_data = sensors_data.copy()
    # print(all_sensors_data)
    threadLock.release()
    # print('sensor_data', sensor_data)
    return sensor_data


# angle1 is 0~180, -180~-0, angle2 is 0~180, -180~-0
def offset_angle(angle1, angle2):
    if (math.fabs(angle1 - angle2) > 180):
        angle = 360 - (math.fabs(angle1) + math.fabs(angle2))
    else:
        angle = math.fabs(angle1) - math.fabs(angle2)
    return math.fabs(angle)


# Data validation: floating between two sets of data does not exceed 10%, if it is right, return true, else return false
def data_validation(sensor_data):
    # print('data_validation', sensor_data)
    global current_sensor_data
    global last_sensor_data
    current_sensor_data = sensor_data
    # print('last_sensor_data', last_sensor_data)
    # print('current_sensor_data', current_sensor_data)
    # assign an initial value to last_sensor_data, when it is the first
    if (last_sensor_data[0] == 0 and last_sensor_data[1] == 0 and last_sensor_data[2] == 0):
        last_sensor_data = current_sensor_data
        return False
    # validate data in the range of 10%
    if (offset_angle(last_sensor_data[0], current_sensor_data[0]) > 10):
        #  print('error 1')
        last_sensor_data = current_sensor_data
        return False
    if (offset_angle(last_sensor_data[1], current_sensor_data[1]) > 10):
        #  print('error 2')
        last_sensor_data = current_sensor_data
        return False
        # height need particularly handle, as its range isn't 0~180,-0~-180
    if (math.fabs(last_sensor_data[2]) - 30 > math.fabs(current_sensor_data[2]) or math.fabs(
            current_sensor_data[2]) > math.fabs(last_sensor_data[2]) + 30):
        #  print('error 3')
        last_sensor_data = current_sensor_data
        return False
    # print('data_validation true')
    return True


# initial system, command dog to stand up until it return 10 sets valid data
def initial_system(sensor_data):
    global num
    global last_sensor_data

    last_sensor_data = current_sensor_data

    # Data validation: floating between two sets of data does not exceed 10%, if it is right, return true, else return false
    def data_validation(sensor_data):
        # print('data_validation', sensor_data)
        global current_sensor_data
        global last_sensor_data
        current_sensor_data = sensor_data
        # print('last_sensor_data', last_sensor_data)
        # print('current_sensor_data', current_sensor_data)
        # assign an initial value to last_sensor_data, when it is the first
        # if (last_sensor_data[0] == 0 and last_sensor_data[1] == 0 and last_sensor_data[2] == 0):
        #     last_sensor_data = current_sensor_data
        #     return False
        # validate data in the range of 10%
        if (offset_angle(last_sensor_data[0], current_sensor_data[0]) > 10):
            #  print('error 1')
            last_sensor_data = current_sensor_data
            return False
        if (offset_angle(last_sensor_data[1], current_sensor_data[1]) > 10):
            #  print('error 2')
            last_sensor_data = current_sensor_data
            return False
            # height need particularly handle, as its range isn't 0~180,-0~-180
        if (math.fabs(last_sensor_data[2]) - 30 > math.fabs(current_sensor_data[2]) or math.fabs(
                current_sensor_data[2]) > math.fabs(last_sensor_data[2]) + 30):
            #  print('error 3')
            last_sensor_data = current_sensor_data
            return False
        # print('data_validation true')
        return True

    if (data_validation(sensor_data)):
        num = num + 1
    else:
        num = 0
    # finish initial system, predictions is 3, or predictions is 4
    global predictions_data
    # print('num', num)
    if (num > 5):
        predictions_data = 3
        return True
    else:
        predictions_data = 4
        return False


def predictions_decision_tree(sensor_data, velocity):
    # print('decision', sensor_data)
    # print('current', current_sensor_data)  # precise data for dog stand up, after intial, it will not be updated
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
            print(current_sensor_data)
    else:
        if (math.fabs(velocity) > 1) :
            print('run')
            # run
            predictions_data = 6
        else :
            # initial sensor datas should be changed by the real deployed environment, so the initial_sensor_data is [-170, -170, 300]. Especially, the inital value of height is invariable.
           # initial_sensor_data = [-173.0, -5.12, 300]
            initial_sensor_data = [-170, -1.0, 300]
            print(initial_sensor_data)
            print((offset_angle(sensor_data[0], initial_sensor_data[0])))
            print((offset_angle(sensor_data[1], initial_sensor_data[1])))
            # height need particularly handle, as its range isn't 0~180,-0~-180
            # if (((math.fabs(sensor_data[2]) < math.fabs(current_sensor_data[2]) - 100) and (offset_angle(sensor_data[0], current_sensor_data[0]) < 10 or (offset_angle(sensor_data[1], current_sensor_data[1]) < 10))) or (math.fabs(sensor_data[2]) < 100)):
            if ((offset_angle(sensor_data[0], initial_sensor_data[0]) > 40) or (offset_angle(sensor_data[1], initial_sensor_data[1]) > 40)):
                    print('down1')
                    # down
                    predictions_data = 2
            else:
                if (((math.fabs(sensor_data[2]) < 100))):

                    print('lay')
                    # lay
                    predictions_data = 0

                else:
                    # up
                    print('up')
                    predictions_data = 1


        threadLock.acquire()
        all_sensors_data['predictions'] = predictions_data
        threadLock.release()
        web_sensors_data = all_sensors_data.copy()
        # print(web_sensors_data)
        return

    threadLock.acquire()
    all_sensors_data['predictions'] = predictions_data
    threadLock.release()
    web_sensors_data = all_sensors_data.copy()


def weblink(c, addr):
    #  print('web', addr)
    try:
        a = pickle.dumps(web_sensors_data)
        c.send(a)
        c.close()
    except EOFError:
        print('eoferror')


def web_server():
    # client server
    server = socket.socket()
    host_server = '0.0.0.0'
    port_server = 12342
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host_server, port_server))
    server.listen(5)

    while True:
        c, addr = server.accept()
        web_t = threading.Thread(target=weblink, args=(c, addr))
        web_t.start()
    server.close()


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    global predictions_data
    # set predictions_data = 4, represent connect
    predictions_data = 4
    # in order to initial system every time, when a new connection is constructed, so set flag = 0
    global flag
    flag = 0

    while True:
        client_data = sock.recv(1024)
        print(client_data)
        if not client_data:
            print('disconnect')

            # set predictions_data = 5, represent disconnect
            predictions_data = 5
            break
        try:
            pickle_data = pickle.loads(client_data)
        except :
            print('pickle.loads error')
            break
            ## return sensor_data(3 kinds of data) and all_sensors_data(7 kinds of data)
        sensor_data = slice_data(pickle_data)
        predictions_decision_tree(sensor_data, velocity)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


def tcp_server():
    #  print('tcp')
    s = socket.socket()
    host = '0.0.0.0'
    port = 12343
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    while True:
        sock, addr = s.accept()
        print('111', addr)
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()



def diff_web_sensors_data():
    global flag_database
    last_web_sensors_data = web_sensors_data
    while (True):
        if (cmp_dict(web_sensors_data, last_web_sensors_data) == 0):
            flag_database = 0
        else:
            flag_database = 1
        last_web_sensors_data = web_sensors_data
        time.sleep(0.5)


def mysql_server():
    # open database
    db = pymysql.connect("localhost", "root", "123", "dog_project")

    # use function cursor() build a object cursor
    cursor = db.cursor()
    while True:

        while (flag_database):
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # SQL insert sentence
            sql = "INSERT INTO dog_tbl (dog_name, yaw_one, \
      yaw_two, pitch_one, pitch_two, roll_one, \
      roll_two, height, time) \
      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  ('p001', web_sensors_data['yaw_one'], web_sensors_data['yaw_two'], web_sensors_data['pitch_one'],
                   web_sensors_data['pitch_two'], web_sensors_data['roll_one'], web_sensors_data['roll_two'],
                   web_sensors_data['height'], dt)

            try:
                # execute sql sentence
                cursor.execute(sql)

                db.commit()
            except:
                # if occur errors, then rollback
                db.rollback()
            time.sleep(1)

    db.close()


# as a tcp server receive the data of dog police pose, also as a web client, send the results of pose
def main():
    try:
        t1 = threading.Thread(target=web_server)
        t2 = threading.Thread(target=tcp_server)
        t3 = threading.Thread(target=mysql_server)
        t1.start()
        t2.start()
        t3.start()
        diff_web_sensors_data()
    except:
        print('Error: unable to start thread')
    while 1:
        pass


if __name__ == "__main__":
    main()
