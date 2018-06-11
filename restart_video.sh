#!/bin/sh

while true

do

ps -ef | grep "gst-launch-1.0" | grep -v "grep"

if [ "$?" -eq 1 ]

then

/home/pi/Documents/run_video.sh & #启动应用，修改成自己的启动应用脚本或命令

echo "process has been restarted!"

else

echo "process already started!"

fi

sleep 20

done


