#!/bin/sh

while true

do

ps -ef | grep "dogs_client_raspberry.py" | grep -v "grep"

if [ "$?" -eq 1 ]

then

/home/pi/Documents/dogs_client_raspberry.py #启动应用，修改成自己的启动应用脚本或命令

echo "process has been restarted!"

else

echo "process already started!"

fi

sleep 5

done
