# -*- coding: utf-8 -*-
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
import pymysql

app = Flask(__name__)

def takedb(tablename): #데이터베이스의 마지막 행 데이터를 가져오기 위한 함수
    conn = pymysql.connect(host='192.168.0.109',
                       user='root',
                       password='root',
                       db='firepre',
                       charset='utf8')
    cur=conn.cursor()
    sql="SELECT %s FROM datas ORDER BY Date DESC LIMIT 1"%(tablename)
    cur.execute(sql)
    last = cur.fetchone()
    for last in last:
        return last
    conn.close

@app.route('/')
def hello_world():
    return render_template('index.html')

#데이터 하나당 flask 사이트에 하나씩 할당
@app.route('/live-data1')
def live_data1():
    # PHP 배열 작성 및 JSON으로 출력
    data = [(time()+32400) * 1000, takedb("wTemp")] #(time()+32400) = 한국 표준시 맞춤
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

#반
@app.route('/live-data2')
def live_data2():
    data = [(time()+32400) * 1000, takedb("Temp")]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data3')
def live_data3():
    data = [(time()+32400) * 1000, takedb("Hum")]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data4')
def live_data4():
    data = [(time()+32400) * 1000, takedb("Co2")]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data5')
def live_data5():
    data = [(time()+32400) * 1000, takedb("Gas")]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data6')
def live_data6():
    data = [(time()+32400) * 1000, takedb("Current")]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
