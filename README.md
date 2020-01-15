# dog_project

[README](README.md) | [中文文档](README_zh.md)

dog_project是一个内网穿透的高性能的警犬姿态识别应用，具有灵敏度高、识别度精确等特点。

<video id="video" controls="" preload="none" poster="http://om2bks7xs.bkt.clouddn.com/2017-08-26-Markdown-Advance-Video.jpg">
<source id="mp4" src="http://om2bks7xs.bkt.clouddn.com/2017-08-26-Markdown-Advance-Video.mp4" type="video/mp4">
</video>

<iframe src="//player.bilibili.com/player.html?aid=34108348&cid=80990288&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

# 目录

<!-- vim-markdown-toc GFM -->

* [部署步骤](#部署步骤)
* [注意事项](#注意事项)
* [资料下载](#资料下载)
* [开发计划](#开发计划)

<!-- vim-markdown-toc -->
## 部署步骤

警犬背心的部署分为两个部分：

* [服务端](#服务端)
* [客户端](#客户端)

### 服务端

(1) 克隆项目

```
git clone https://github.com/ZhuChaozheng/dog_project.git
```

(2) 进入文件夹并移动后端和网页服务至/var/www/html

```
cd dog_project && mv /html/ /var/www/html
```

(3)搭建nginx服务器和lighttpd服务器分别提供视频和web服务

下载nginx

```
sudo apt-get install nginx
```

将进入工程文件夹将nginx.conf移到/etc/nginx/下

```
mv ./nginx.conf /etc/nginx
```

启动nginx服务器

```
sudo /etc/init.d/nginx start
```

下载lighttpd

```
apt-get install lighttpd
```

启动lighttpd

```
./lighttpd -f ../config/lighttpd.conf
```

(4) 启动服务端数据接收

```
python3 dogs_server_blackant.py
```

### 客户端(树莓派)

运行树莓派客户端文件

```
python3 dogs_client_raspberry.py
```

运行run_video.sh推流视频
```
./run_video.sh
```

## 注意事项
我们所使用的数据网关的id以及密码如下
```
ssid=HUAWEI-5F42
psk=34127615
```
当然，熟悉Linux环境的您也可以通过以下命令查看配置文件并修改我们预设配置
```
sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
```
## 资料下载
目前我们的系统镜像托管于百度云盘
```
链接：https://pan.baidu.com/s/1mKjUmRVHnB2NxapOAziL0A 
提取码：rrdn 
```
## 开发计划
目前第一代警犬项目基本已经完工了，第二代正在建设中，详见<dogs_server_blackant_second_version.py>，如有建议，欢迎来反馈.

