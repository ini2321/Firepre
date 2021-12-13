import random
import time
from typing import Tuple
import numpy as np
from numpy.core import numeric
import paho.mqtt.client as mqtt_client
import csv
from datetime import datetime
import pymysql

# broker 정보
broker_address = "192.168.0.36"
broker_port = 1883

topic = "outTopic"

#마리아DB 연결(로컬호스트, root, DB이름 = firepre)
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='firepre',
                       charset='utf8')

#클라이언트 만들기
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        # print(f"log: {1}")
        print("")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #msg.payload.decode()에서 메세지와 토픽을 받음
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        payload = msg.payload.decode()
        InsertDB(payload)


        # return payload
    client.subscribe(topic) #1
    client.on_message = on_message

def InsertDB(data):
    print(data)
    real = data.split(',')
    a,b,c,d,e,f,g = real
    cur = conn.cursor()
    #DB에 센서값 넣음
    #NOW() = 시간, a = 방수온도센서, b = 온습도의 온도, c = 온습도의 습도, d = 이산화탄소 농도, e = 이산화탄소센서 온도, f = 가스농도, g = 전류
    cur.execute("INSERT INTO datas(Date,wTemp,Temp,Hum,Co2,CoTemp,Gas,Current) \
            VALUES(NOW(), %s, %s, %s, %s, %s, %s, %s)"
            ,(a, b, c, d, e, f, g)
            )
    conn.commit()

def run():
    client = connect_mqtt()
    subscribe(client)   
    client.loop_forever()
  

if __name__ == '__main__':
    run()
