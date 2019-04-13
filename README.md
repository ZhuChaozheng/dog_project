# dog_project

[README](README.md) | [中文文档](README_zh.md)

dog_project是一个内网穿透的高性能的警犬姿态识别应用，具有灵敏度高、识别度精确等特点。

# 目录

<!-- vim-markdown-toc GFM -->

* [开发状态](#开发状态)
* [架构](#架构)
* [功能说明](#功能说明)
* [开发计划](#开发计划)

<!-- vim-markdown-toc -->

## 开发状态

目前第一代警犬项目基本已经完工，您可以在最新版本中试用它。

第二代警犬项目目前正在开发当中，敬请期待。

## 架构

![architecture](/README_img/const.png)

## 功能说明
### 1 服务端接受客户端数据（姿态、影像等）并判断姿态
*接受数据*
```
 t2 = threading.Thread(target=tcp_server)
 t2.start()
 diff_web_sensors_data()
```

*判断姿态*
接收:
```
client_data = sock.recv(1024)
#        print(client_data)
        if not client_data:
            print('disconnect')
```


处理:
```
sensor_data = slice_data(pickle_data)
```

判断警犬姿态:
```
predictions_decision_tree(sensor_data, velocity)
```



### 2 数据库线程将新值写入数据库


```
def mysql_server():
...
...
	cursor.execute(sql)
	 db.commit()
```

### 3 服务端接收到web端请求后，将数据库最新一条数据发送

```
def tcp_server():
...
...
	sock, addr = s.accept()
		print('tcp client addr: ', addr)
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()
```

### 4 模拟数据请求
在客户端未开启状态下发送模拟数据给服务端

```
  host = 'server.blackant.org'
  port = 10011

  r = ['00', '1e', '6c', '01', 'ea', '44', '00', 'e2', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c', '6c', '01', 'ea', '44', '00', 'e2', '6c']
  flag = 0
  ...
  ...
while True:
        #print('ii', r)
        if (flag == 0):
            r = ['01', 'ea', '41', '01', 'ea', '41', '01', 'ea', '41', '01', 'ea', '41', '01', 'ea', '41', '01', 'ea', '41', 'ea', '44', '01', 'ea', '41']
            flag = 1
            print('0')
        else:
            flag = 0
            r = ['6c', '00', 'e0', '6c', '6c', '00', 'e0', '6c', '6c', '00', 'e0', '6c', '6c', '01', '6c', '00', 'e0', '6c', '6c', '01', 'e0', '6c', '6c']
            print('1')
#        a = json.dumps(r).encode('utf-8')
        r.append('p001')
        a = pickle.dumps(r)
        try:
            s.send(a)
        except:
            print('connect break')
            s.close()
            break
        time.sleep(1)    
```

### 5 客户端从串口读取数据并发送给服务端
```
  x = serial.Serial('/dev/ttyUSB0', 115200)
```

```
s = socket.socket()
    host = 'server.blackant.org'
    # host = '180.109.138.23'
    port = 12343
    s.connect((host, port))

...
...
 a = pickle.dumps(r)
            s.send(a)
```
### 6 web端显示相关数据
![http://server.blackant.org:8000/](/README_img/web.png)

## 开发计划
目前第一代警犬项目基本已经完工了，第二代正在建设中，详见<dogs_server_blackant_second_version.py>，如有建议，欢迎来反馈.
