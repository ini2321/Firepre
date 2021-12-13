#1. 마리아DB 연결 후 데이터베이스 작성 프로그램
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       charset='utf8')

#friepre 이름의 데이터베이스 생성
with conn:
    with conn.cursor() as cur:
        cur.execute('CREATE DATABASE firepre')
        conn.commit()

