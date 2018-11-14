# dog_project
A project for recognition dog pose

for a video demo, please visit https://www.bilibili.com/video/av34108348?share_medium=android&share_source=copy_link&bbid=452131F3-C84D-4DF0-89AF-AA0107CE68FF16810infoc&ts=1539869227641

# nginx
this server for live video from dog helmet

## nginx.conf
use this conf file to replace the default conf file in /etc/nginx/

## live video on raspi
see https://blog.gtwang.org/iot/raspberry-pi-nginx-rtmp-server-live-streaming/   for detail

# lighttpd
this server for the visualization of dog pose

firstly, it support for python3. secondly, place all the files of html in the /var/www/html.

# start system by self when machine running
please add those commands in your rc.local file(/etc/rc.local), 

    /usr/bin/python3 /home/blackant/Documents/dogs_server_blackant.py &
    /etc/init.d/nginx start



# Supplements

## dogs_client_raspberry_test.py 
used as a tool for feature testing

## System Architecture
sensor data(raspberry_client.py) -> server (raspberry_server.py) -> 
