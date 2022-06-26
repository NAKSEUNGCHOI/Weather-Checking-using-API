from flask import Flask, request
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
api = Api(app)

class TodoSimple(Resource):
  def get(self, weather):
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      port="3306",
      user="root",
      password="",
      database="final",
      auth_plugin="mysql_native_password"
    ) #mysql 접속문
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dingdong") #dingdong이라는 테이블에 있는 모든 데이터를 선택
    myresult = mycursor.fetchall() # 선택된 데이터를 출력
    data = myresult
    return data #데이터를 리턴함
    
api.add_resource(TodoSimple, '/<string:weather>') #주소설정

if __name__ == '__main__': #restful 실행
  app.run(debug=True)