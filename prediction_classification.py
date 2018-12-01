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

# define some useful global variable, which we don't need to modify them in the blew functions.
initial_sensor_data = -3
# pose status variable
running = 0
stand_up = 1
sit_down = 2
lay = 3


# we should modified the variable value in below functions, so set variable as global.
# default, we think the initial pose is stand up,
last_pose = stand_up
current_pose = stand_up


# this method is used to decode the communication protocal.
# sensor_data_raw include three variables, accelerated_velocity, angular_velocity,
# pitch. However, the variable of sensor_data_raw is encoded for transpotation, so,
# now, we should decoded it. after decoding, the value will be stored in sensor_data.

web_sensor_data = {'accelerated_velocity': 0, 'angular_velocity': 0, 'pitch': 0, 'current_pose': 0, 'status': 0}
def slice_data(sensor_data_raw):
    sensor_data = {'accelerated_velocity': 0, 'angular_velocity': 0, 'pitch': 0}
    global web_sensor_data

    if len(sensor_data_raw) < 10:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # slice the accelerated_velocity value from the sensor_data_raw
    accelerated_velocity_str = ''.join(sensor_data_raw[0:2])
    accelerated_velocity_int = int(yaw_str, 16)
    accelerated_velocity_sign = int(sensor_data_raw[2], 16)
    if accelerated_velocity_sign == 0:
        accelerated_velocity_int = accelerated_velocity_int
    else:
        accelerated_velocity_int = -accelerated_velocity_int
    accelerated_velocity_int = accelerated_velocity_int / 100
    sensor_data['accelerated_velocity'] = accelerated_velocity_int
    web_sensor_data['accelerated_velocity'] = accelerated_velocity_int

    # slice the angular_velocity value from the sensor_data_raw
    angular_velocity_str = ''.join(sensor_data_raw[3:5])
    angular_velocity_int = int(angular_velocity_str, 16)
    angular_velocity_sign = int(sensor_data_raw[5], 16)
    if angular_velocity_sign == 0:
        angular_velocity_int = angular_velocity_int
    else:
        angular_velocity_int = -angular_velocity_int
    angular_velocity_int = angular_velocity_int / 100
    sensor_data['angular_velocity'] = angular_velocity_int
    web_sensor_data['angular_velocity'] = angular_velocity_int

    # slice the pitch value from the sensor_data_raw
    pitch_str = ''.join(sensor_data_raw[6:8])
    pitch_int = int(pitch_str, 16)
    pitch_sign = int(sensor_data_raw[8], 16)
    if pitch_sign == 0:
        pitch_int = pitch_int
    else:
        pitch_int = -pitch_int
    pitch_int = pitch_int / 100
    sensor_data['pitch'] = pitch_int
    web_sensor_data['pitch'] = pitch_int


    return sensor_data

# this function is used to calculate the offset value between two angles.
# angle1 is 0~180, -180~-0, angle2 is 0~180, -180~-0
def offset_angle(angle1, angle2):
    if (math.fabs(angle1 - angle2) > 180):
        angle = 360 - (math.fabs(angle1) + math.fabs(angle2))
    else:
        angle = math.fabs(angle1) - math.fabs(angle2)
    return math.fabs(angle)


# this function try to predict the current pose, mainly depend on two conditions,
# the last pose and current action. Specifically, the last pose include those
# states, which are stand up, sit down, lay, and running. For current action, it
# includes those actions, which are accelerated_velocity, angluar_velocity, angle
# offset. In order to calibrate the initial pose, we should command the dog to run
# as soon as possible. when the angluar_velocity is greater than 1, it must be
# running.

# sensor_data: accelerated_velocity, angular_velocity, pitch


# web_sensor_data
def predictions_classification(sensor_data):
    # since we will modify those variables value in the next steps, we define a global
    # before them.
    global last_pose
    global current_pose
    global web_sensor_data
    # accelerated_velocity is used to classificate the pose of stand up or lay
    # when the last time is sit down
    accelerated_velocity = sensor_data[0]
    # angluar_velocity is used to classificate the pose of running
    angular_velocity = sensor_data[1]

    # initial_sensor_data[2] default is -3, now the pose is stand up or lay
    angle_offset = offset_angle(sensor_data[2], initial_sensor_data)

    # now, let us definite a thing that must happen when the angular_velocity
    # is greater than 1. it must be running. So, in order to initial our
    # system, when should command the dog to run as soon as possible.
    if angular_velocity > 1:
        current_pose = running
        print("running")

    else:

        # last_pose is stand_up, then the current_pose could among sit_down,
        # stand_up, and running. When the angular_velocity is bigger than 1, it
        # must be running. When the angle_offset is greater than 40, it must be
        # sit_down. Or it shoule be keep the same pose. However, when the sensor data
        # enter this function, it immediately hanle the variable of angular_velocity.
        # if it is greater than 1, it must be running.
        if last_pose == stand_up:
            if angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            elif accelerated_velocity > 10:
                current_pose = lay
                print("lay")
            else:
                current_pose = stand_up
                print("stand_up")

        # last_pose is running, then the current_pose must between running and
        # stand_up. When the angular_velocity is greater than 1, it must be keep
        # running. Or it shoule be stand_up. However, when the sensor data
        # enter this function, it immediately hanle the variable of angular_velocity.
        # if it is greater than 1, it must be running.
        elif last_pose == running:
            current_pose = stand_up
            print("stand_up")

        # last_pose is sit_down, then the current_pose could among stand_up,
        # sit_down and lay. When comparing initial_sensor_data value(stand up),
        # the angle_offset is greater than 40, it must be sit_down. When the
        # accelerated_velocity is greater than 10, it must
        # be lay, since we place the sensor(only an IMU) on the front back of
        # dog. Or it shoule be stand_up, as the sensor's accelerated_velocity
        # keep in a stable range. this range must less than 10.

        elif last_pose == sit_down:
            if angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            elif accelerated_velocity > 10:
                current_pose = lay
                print("lay")
            else:
                current_pose = stand_up
                print("stand_up")

        # last_pose is lay, then the current_pose could between lay and sit_down.
        # When the accelerated_velocity is greater than 10, or angle_offset is
        # greater than 40, it must be sit_down. Or current_pose should keep lay.
        elif last_pose == lay:
            if accelerated_velocity > 10:
                current_pose = stand_up
                print("stand_up")
            elif accelerated_velocity > 10 and angle_offset > 40:
                current_pose = sit_down
                print("sit_down")
            else:
                current_pose == lay
                print("lay")

    last_pose = current_pose
    # now, web_sensor_data inherit all the data from sensor_data, accelerated_velocity,
    # angular_velocity, pitch and current_pose
    web_sensor_data.append(current_pose)


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

# main steps:
# 1. wait for connecting from clients
# 2. receive raw sensor data
# 3. slice raw sensor data to actual data(accelerated_velocity, angular_velocity,
# pitch)
# 4. execute predictions_classification function

normal = 0
abnormal = 1
# globla variable for indicating system status
status = normal

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    global status
    global web_sensor_data
    # set status as normal, represent connect
    status = normal

    while True:
        client_data = sock.recv(1024)
        print(client_data)
        if not client_data:
            print('disconnect')
            # set status as abnormal, represent disconnect
            status = abnormal
            break
        try:
            pickle_data = pickle.loads(client_data)
        except :
            print('pickle.loads error')
            break

        ## return sensor_data(accelerated_velocity, angular_velocity, pitch)
        sensor_data = slice_data(pickle_data)
        predictions_classification(sensor_data)

        # now, web_sensor_data inherit all the data from sensor_data, accelerated_velocity,
        # angular_velocity, pitch and current_pose, status
        web_sensor_data['status'] = status
    sock.close()
    print('Connection from %s:%s closed.' % addr)


def web_server():
    # client server
    server = socket.socket()
    host_server = '0.0.0.0'
    port_server = 12342
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host_server, port_server))
    server.listen(5)

    while True:
        client, addr = server.accept()
        web_t = threading.Thread(target=weblink, args=(client, addr))
        web_t.start()
    server.close()

def weblink(client, addr):
    try:
        # for debug, web_sensor_data consists of the latest values of accelerated_velocity,
        # angular_velocity, pitch, current_pose, and status.
        print(web_sensor_data)
        encoded_data = pickle.dumps(web_sensor_data)
        client.send(encoded_data)
        client.close()
    except EOFError:
        print('eoferror')

# since we want store the useful sensor data in database, so we should determinate
# whether the data has changed.
def diff_web_sensor_data():
    global flag_database
    last_web_sensor_data = web_sensor_data
    while (True):
        if (cmp_dict(web_sensor_data, last_web_sensor_data) == 0):
            flag_database = 0
        else:
            flag_database = 1
        last_web_sensor_data = web_sensor_data
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

            sql = "INSERT INTO dog_second_version (dog_name, accelerated_velocity, \
            angular_velocity, pitch, time) \
      VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                  ('p001', web_sensors_data['accelerated_velocity'], \
                  web_sensors_data['angular_velocity'], web_sensors_data['pitch'], dt)

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
