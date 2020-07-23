#!/usr/bin/env python  
# coding=utf-8
# 为了能在外部脚本中调用Django ORM模型，必须配置脚本环境变量，将脚本注册到Django的环境变量中
import os, sys
import django

# 第一个参数固定，第二个参数是工程名称.settings
os.environ.setdefault('DJANGO_SETTING_MODULE', 'mqtt.settings')
django.setup()

# 使用独立线程运行
from threading import Thread
from server import models
from server import views
import json
import sys
import os
import time
import paho.mqtt.client as mqtt

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")

REPORT_TOPIC = 'DeviceToServer/#'  # 主题
PUBLISH_TOPIC = 'ServerToDevice/'
Client = None

def server_send(client, topic, message: str):
    """
    客户端发布消息
    :param self:
    :param client: 连接信息
    :param topic: 主题
    :param message: 消息主体
    :return:
    """
    time_now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    payload = {"msg": "%s" % message, "data": "%s" % time_now}
    # publish(主题：Topic; 消息内容)
    client.publish(topic, json.dumps(payload, ensure_ascii=False))
    print("Successful send message!")
    return True

def server_to_device_send(id,msg):
    server_send(Client,PUBLISH_TOPIC+id,msg)
    return True

def on_connect(client, userdata, flags, rc):
    print('connected to mqtt with resurt code ', rc)
    client.subscribe(REPORT_TOPIC)  # 订阅主题


def on_message(client, userdata, msg):
    """
    接收客户端发送的消息
    :param client: 连接信息
    :param userdata: 
    :param msg: 客户端返回的消息
    :return: 
    """
    global Client
    print("mqtt server!")
    print(msg.topic)
    payload = json.loads(msg.payload.decode('utf-8'))
    print(payload)
    toDeviceTopic = str(msg.topic).replace('DeviceToServer/', PUBLISH_TOPIC)
    deviceID = str(msg.topic).replace('DeviceToServer/', '')
    views.orm_create(deviceID,payload)
    print(toDeviceTopic)
    server_send(Client, toDeviceTopic, '还差点')


def server_conenet(client):
    client.on_connect = on_connect  # 启用订阅模式
    client.on_message = on_message  # 接收消息
    client.connect("47.105.187.66", 1883, 60)  # 链接
    # client.loop_start()   # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
    # client.loop_forever(retry_first_connection=True)   # 以forever方式阻塞运行。有掉线重连功能

# mqtt客户端启动函数
def mqttfunction():
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    # client.loop_start()
    # client.loop_forever() 有掉线重连功能
    global Client
    Client.loop_forever(retry_first_connection=True)


def server_stop(client):
    client.loop_stop()  # 停止服务端
    sys.exit(0)


def server_main():
    global Client
    # client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    client_id = 'django-client'
    Client = mqtt.Client(client_id, transport='tcp')
    # 启动
    server_conenet(Client)
    mqttthread = Thread(target=mqttfunction)
    mqttthread.start()


if __name__ == '__main__':
    # 启动监听
    server_main()
