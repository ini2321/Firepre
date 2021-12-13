# 2. 새 테이블 작성 프로그램
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='firepre', #1번에서 만든 데이터베이스 이름
                       charset='utf8')


#테이블 안의 열(속성) 생성
sql = '''CREATE TABLE datas ( 
        Date varchar(255),
        wTemp float,
        Temp float,
        Hum float,
        Co2 float,
        CoTemp float,
        Gas float,
        Current float
        )
        '''

with conn:
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
