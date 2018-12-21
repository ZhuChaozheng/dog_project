#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 引入必要的module
import serial
import socket
import pickle
import time


def main():
    # read serial
    x = serial.Serial('/dev/ttyUSB0', 115200)
    r = []
    num = 0
    num1 = 0
    length = 0
    j = 0
    s = socket.socket()
    host = 'server.blackant.org'
    # host = '180.109.138.23'
    port = 12343
    s.connect((host, port))
    while True:
        str_read = x.read()
        #  print(str_read)
        i = ['%02x' % b for b in str_read]
        # print(str_read_byte)
        print(i)
        if i[0] == 'aa' and num == 0:
            num = num + 1
            continue
        elif i[0] == 'aa' and num == 1:
            num = num + 1
            continue
        elif i[0] == 'f1' and num == 2:
            num = num + 1
            continue
        if num == 3:
            length = int(i[0], 16)
            num = num + 1
            continue
        if num > 3 and num < 26:
            r.extend(i)
            num = num + 1
            if len(r) == 21:
                print('ii', r)

            a = pickle.dumps(r)
            s.send(a)
            time.sleep(1)
        if num == 26:
           num = 0
           num1 = 0
           r = []
    s.close()


if __name__ == "__main__":
    main()


