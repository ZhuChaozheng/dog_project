#!/bin/sh 
gst-launch-1.0 -v v4l2src ! queue ! videoconvert ! omxh264enc !  h264parse ! flvmux ! rtmpsink location='rtmp://server.blackant.org:1935/live/hello live=1'
