from flask import Flask, request, jsonify

import sys

application = Flask(__name__)


@application.route("/")

def hello():

    return "Hello goorm!"


@application.route('/course',methods=['POST'])

def course():

    req = request.get_json()
    
    course_name = req["action"]["detailParams"]["course"]["value"]
    
    if course_name == "수학":
    
        answer = "메가스터디 현우진 들으면 될 듯해"
    
    elif course_name == "영어":
    
        answer = "대성마이맥 이명학 들으면 될 듯해"
    
    elif course_name == "국어":
    
        answer = "기출문제를 많이 풀어보는게 어때?"
    
    elif course_name == "과학":
        
        answer = "교과서를 잘 읽어보는게 어때?"
    
    elif course_name == "사회":
    
        answer = "교과서를 잘 읽어보는게 어떄?"
        
    res = {
        
        "version": "2.0",
        
        "template": {
        
            "outputs": [
            
                {
                
                    "simpleText": {
                    
                        "text": answer
                    
                    }
                    
                }

            ]
        
        }
    
    }
    
    return jsonify(res)

import requests

def naver_local_search(query, display):
    
    headers = {
    
        "X-Naver-Client-Id" : "HgynKDsE4dyMbKYhNzxc",
        
        "X-Naver-Client-Secret" : "Gg5sh49eCC"
        
    }

    params = {
        
        "sort" : "comment",
        
        "query" : query,
        
        "display" : display
        
    }
    
    naver_local_url = "https://openapi.naver.com/v1/search/local.json"
    
    res = requests.get(naver_local_url, headers=headers, params=params)
    
    places = res.json().get('items')
    
    return places

@application.route("/location",methods=['Post'])

def location():
    
    req = request.get_json()
    
    location = req["action"]["detailParams"]["location"]["value"]
    
    place = '약국'
    
    recommends = []
    
    query = location + " " + place
    
    result_list = naver_local_search(query, 3)
    
    for el in result_list:
        
        el_title = el['title'].replace("</b>", " ").replace("<b>", " ")
        
        el_address = el['address']
        
        recommends.append([el_title, el_address])
        
    str1 = "현재 " + str(location) + "에서 가장 괜찮은 약국 3곳을 추춘해줄게. 빠르게 약국을 다녀와.\n"
    
    str2 = "1. 이름: " + recommends[0][0] + ", 주소: " + recommends[0][1] + '.\n'
    
    str3 = "2. 이름: " + recommends[1][0] + ", 주소: " + recommends[1][1] + '.\n'
    
    str4 = "3. 이름: " + recommends[2][0] + ", 주소: " + recommends[2][1] + '.\n'
    
    answer = str1 + str2 + str3 + str4

    res = {
        
        "version": "2.0",
        
        "template": {
            
            "outputs": [
                
                {
                    
                    "simpleText": {
                        
                        "text": answer
                        
                    }

                }
                
            ]
            
        }
        
    }
    
    return jsonify(res)
    
    
import urllib

import requests

import json

@application.route("/rec1",methods=['POST'])

def rec1():

    req = request.get_json()

    price = req["action"]["detailParams"]["price"]["value"]	# json파일 읽기

    price = eval(price)

    price = price["amount"] # 단위 원만 취급

    kind = req["action"]["detailParams"]["kind"]["value"]	# json파일 읽기    

    query = kind

    query = urllib.parse.quote(query)

    display = "100" # 변경가능

    url = "https://openapi.naver.com/v1/search/shop?query=" + query + "&display=" + display

    request_ = urllib.request.Request(url)

    request_.add_header('X-Naver-Client-Id', "U02F3kzfdGv63gNLkq_n")    

    request_.add_header('X-Naver-Client-Secret', "jOIxt6J8Op")

    response = urllib.request.urlopen(request_)  

    res = json.loads(response.read().decode('utf-8'))

    #print(res)

    answer = "가격을 변경해서 검색해줘"

    items = []

    for item in res["items"]:

        if int(item["lprice"]) >= int(price)*0.9 and int(item['lprice']) <= int(price)*1.1: # 범위 설정 자유롭게

            items.append([item["title"].replace("</b>", " ").replace("<b>", " "), item["link"]])
            
            if len(items) == 3: # 이름이나 이미지로도 할 수 있음
                
                break # 여러개 할 수도 있음

    str1 = "말한 조건에 맞는 선물 3개를 추천해줄게.\n"
    
    str2 = "1. 이름: " + items[0][0] + ", 링크: " + items[0][1] + '.\n'
    
    str3 = "2. 이름: " + items[1][0] + ", 링크: " + items[1][1] + '.\n'
    
    str4 = "3. 이름: " + items[2][0] + ", 링크: " + items[2][1] + '.\n'
    
    answer = str1 + str2 + str3 + str4
               
        #print(item['lprice']) # 실험용

    # 답변 텍스트 설정

    res = {

        "version": "2.0",

        "template": {

            "outputs": [

                {

                    "simpleText": {

                        "text": answer

                    }

                }

            ]

        }

    }



    # 답변 전송

    return jsonify(res)    
    
import openpyxl

import numpy as np

from sklearn.preprocessing import StandardScaler

@application.route("/rec2", methods=['POST'])

def rec2():

    req = request.get_json()
    
    price = req["action"]["detailParams"]["price"]["value"]	# json파일 읽기

    price = eval(price)

    price = price["amount"] # 단위 원만 취급

    age = req["action"]["detailParams"]["age"]["value"]	# json파일 읽기
    
    age = eval(age)
    
    age = age["amount"]
    
    wb = openpyxl.load_workbook('./rec_ex.xlsx')
    
    ws = wb.active
    
    items = []
    
    for row in ws.iter_rows():
        
        data = []
        
        for cell in row:
            
            data.append(cell.value)
            
        items.append(data)
        
    items = items[1:]
    
    items.append(['tmp', price, age])
    
    xys = np.array(items)[:,1:]
    
    standardScaler = StandardScaler()
    
    standardScaler.fit(xys)
    
    train_data_standardScaled = standardScaler.transform(xys)
    
    res_min = 1e10
    
    idx = -1
    
    for i, xy in enumerate(train_data_standardScaled[:-1]):
        
        if res_min > np.linalg.norm(train_data_standardScaled[-1] - xy):
            
            res_min = np.linalg.norm(train_data_standardScaled[-1] - xy)
            
            idx=i
            
    answer = items[idx][0] + " 추천해드립니다."
    
    res = {

        "version": "2.0",

        "template": {

            "outputs": [

                {

                    "simpleText": {

                        "text": answer

                    }

                }

            ]

        }

    }

    # 답변 전송
    return jsonify(res)    
  
if __name__ == "__main__":
    
    application.run(host='0.0.0.0', port=5000, threaded=True)
    
    
    
    
    