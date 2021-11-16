import socket
import random
import requests
from pprint import pprint
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
city = input("Enter your city: ") 
#Users have access to selecting a city where they would like to get the weather info.
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=37ce5c66e50b1512d8a23f5757a376b7&units=metric'.format(city)
#Using api, bring the weather data in url from the website, openweathermap.com
res = requests.get(url) 
data = res.json() #url to json
stop = "y"

while True:
    msg = input("If you want to get the current weather info, press anything. To quit, press y: ") 
    #blocking excessive amount of data from going into mysql, and quit when type "y" 
    if msg == stop:
        print("Quit program. ")
        break
    else:
        country = str(data['sys']['country'])
        temp = str(data['main']['temp'])
        feelslike = str(data['main']['feels_like'])
        humid = str(data['main']['humidity'])
        wind = str(data['wind']['speed'])
        weather = str(data['weather'][0]['main'])
        description = str(data['weather'][0]['description'])
        #api로 받아온 무수히 길고 복잡한 데이터를 각각의 변수를 생성해 필요한 데이터만 변수에 저장하는 코드.
        x = dict(country = country, city = city, temperature = temp, feels = feelslike, humidity = humid, wind = wind, cloudiness = description)
        #필요한 데이터만 변수들에 저장한 후 이 변수들을 dict 타입으로 생성한 x변수에 삽입.
        DictToString = str(x) #서버로 보내기 위해 dict 타입인 x변수를 string 타입으로 변경.
        sock.sendto(DictToString.encode(), ("127.0.0.1", 3306)) #전송
        recvMsg, addr = sock.recvfrom(8888) #client에서 보낸 파일이 server에 갔다가 다시 돌아옴
        ToDict = eval(recvMsg) #서버로 부터 바이트형식으로 다시 돌아온 데이터를 dict형태로 바꿈
        print(ToDict == x) #dict형태로 바꾼 데이터를 기존에 보냈던 파일과 boolean으로 같은지 확인.
    

sock.close()

