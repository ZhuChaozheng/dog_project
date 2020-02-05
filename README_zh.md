dog_project
===========

[README](README.md) | [中文文档](README_zh.md)

基于多传感器数据背心的警犬位姿实时重建与仿真，具有易穿戴、实时性好、高可靠性、高精度、支持4G网络等特点。在4G网络环境稳定的情况下，系统时延小于1s。系统基于多传感器网络的警犬姿态检测与重建，能够实时高精度反映警犬在反恐搜爆实战中的当前姿态信息，从而在远距离指挥当中更大效率地利用警犬的机动性、高准确性，从而进一步降低安全隐患。

目录
========


* [视频演示](#jump_1)

* [项目环境](#jump_2)

* [系统架构](#jump_3)

* [克隆项目](#jump_4)

* [系统搭建](#jump_5)

* [系统展示](#jump_6)

* [未来规划](#jump_7)

* [注意事项](#jump_8)

* [附录](#jump_9)


视频演示
===========

<span id="jump_1">[![](doc/pic/dog_project_cover.gif)](https://youtu.be/jjddJISvFiA)</span>

<span id="jump_2">项目环境</span>
===========

> 硬件：1个树莓派3B+、2个IMU传感器、一个充电宝、警犬马甲

> 软件：Ubuntu系统、nginx服务器、lighttpd服务器、python3

<span id="jump_3">系统架构</span>
===================

数据背心内装有摄像头和 imu 传感器，可以方便地收集到狗身体的第一人称视觉(fpv)视频和的加速度、角速度数据。 然后，树莓派 (客户端)作为中间件将收集到的狗的姿态和视频数据发送到远程服务器(域名:  server.blackant.org )。 Nginx 服务器用于播放 rtmp 视频流，lighttpd 服务器根据训练后的知识同时分析信任姿态，并在流行的浏览器(例如firefox、 safari 等)上显示狗的姿态和数据。

![](doc/pic/arch_illustration.gif)

<span id="jump_4">克隆项目</span>
=============

`git clone: https://github.com/ZhuChaozheng/dog_project.git`

<span id="jump_5">系统搭建</span>
============

 服务器
-------

1. 进入文件夹并移动后端和网页服务至/var/www/html

   `cd dog_project && mv /html/ /var/www/html`

2. 搭建nginx服务器和lighttpd服务器分别提供视频和web服务

   下载nginx

   `sudo apt-get install nginx`

​		将进入工程文件夹将nginx.conf移到/etc/nginx/下

​		`mv ./nginx.conf /etc/nginx`

​		启动nginx服务器

​		`sudo /etc/init.d/nginx start`

​		下载lighttpd

​		`apt-get install lighttpd`

​		启动lighttpd

​		`./lighttpd -f ../config/lighttpd.conf`

客户端（树莓派）
--------------------

运行树莓派客户端文件

`python3 dogs_client_raspberry.py`

运行run_video.sh推流视频

`./ run_video.sh`

系统展示
=======

<span id="jump_6">[![](doc/pic/web.gif)](http://server.blackant.org:8000)</span>

<span id="jump_7">未来规划</span>
=======

待更新。。。

<span id="jump_8">注意事项</span>
=========

1. 浏览器需要先开启flash才能看到视频流

2. 我们所使用的数据网关的id以及密码如下：

   - ssid=HUAWEI-5F42
   - psk=34127615

3. 修改配置

   `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`

<span id="jump_9">附录</span>
========

目前我们的系统镜像托管于百度云盘

链接：https://pan.baidu.com/s/1mKjUmRVHnB2NxapOAziL0A

提取码：rrdn
