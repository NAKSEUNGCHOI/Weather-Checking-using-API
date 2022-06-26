import socket
import mysql.connector
import ast
import datetime

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="",
    database="final",
    auth_plugin="mysql_native_password"
) #mysql 연결

mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE TABLE dingdong (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))") 
except:
    pass
#최초 mysql에서 dingdong이라는 테이블 생성(추후에 heidisql에서 직접 데이터 카테고리명 수정과 추가를 함)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 3306))
#서버 오픈하여 IP와 port를 지정

while True:
    print('\nwaiting to receive message')
    data, addr = sock.recvfrom(1024) ##client로 부터 데이터를 받음
    print("Server is connected!") #서버 연결 됐는지 확인하는 프린터문
    data = data.decode() #byte 타입에서 string 타입으로 변경
    sock.sendto(data.encode(), addr) #client측에서 온 데이터를 다시 보내 데이터가 잘 왔는지 확인하기 위한 문구
    ToDict = eval(data) #기존에 Dict에서 String 타입으로 바꾼것을 server에서 사용하기 위해 다시 dict 타입으로 변경
    time = datetime.datetime.now() #현재시간 생성
    print('receive {} bytes from {}.'.format(len(data), addr)) #얼마의 바이트가 어느 주소로 부터 왔는지 확인.
    sql = "INSERT INTO dingdong (country, city, temperature, feels, humidity, wind, cloudiness, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    #sql이라는 변수에 country, city, temperature 등의 데이터를 dingdong이라는 테이블에 삽입하는 문
    val = (ToDict["country"], ToDict["city"], ToDict["temperature"], ToDict["feels"], 
                            ToDict["humidity"], ToDict["wind"], ToDict["cloudiness"], time)
    #Val이라는 변수를 생성해 위에서 dict 타입으로 재변경한 데이터 값들을 tuple형식으로 저장.
    mycursor.execute(sql, val)
    #val 데이터를 sql(mysql)로 삽입
    mydb.commit() 
    print(mycursor.rowcount, "record inserted.") #mysql로 잘 저장되었는지 확인하는 프린터 문.