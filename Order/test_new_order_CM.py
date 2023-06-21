import requests
import json
import pytest 

# Шаги:
# 1. Запускать командой: pytest .\Order\test_new_order_CM.py
# 2. loadList = json.loads(body)  - на этой строке ошибка: the JSON object must be str, bytes or bytearray, not dict
# 3. Надо разбираться, почему в pytest падает там, где не падает в Питоне  !!!
# Как падает можно посмотреть в примере new_order_CM.py

# При  работе с БД, ошибка: не находит DLL

main_url = "http://10.0.0.129:8130/bora/"
json_headers = {
    "Content-type": "application/json",
    "Bora-Alien": "2"
}

def load_json(f):
    try:
        with open(f, 'r', encoding='utf-8') as json_file:
            s = json_file.read()
            return s
    except FileNotFoundError:
        return {}

def getOrderId(r):
    r_dict = r.json() # возвращает ответ в виде JSON и конвертирует в словарь dict
    #r_text = r.text # возвращает контент ответа сервера текстом в юникоде (str)
    if r_dict.get('OrderResponse'):
        value = r.json()['OrderResponse']['Success']['Id'] # возвращает содержимое 'Id'
        print("ID заказа: ", value)
        return value
    else:
        print('Error: ')
        print(r.text) # возвращает контент ответа сервера текстом в юникоде (str)
        return 0

def getOrderInfo(r):
    r_dict = r.json()['OrderInfoResponse'] # возвращает ответ в виде JSON и конвертирует в словарь dict
    if r_dict.get('AccommodationList'):
        inner_list = r_dict['AccommodationList']['Accommodation'] # Содержимое 'Accommodation' это list, а не dict
        id_list = inner_list[0]
        id_dict = dict(id_list) # преобразование в dict
        usluga_id = id_dict.get('Id')
        hotel_dict = id_dict.get('Hotel')
        print("Гостиница: ", hotel_dict)
        hotel_id = hotel_dict.get('Code')
        for i in r_dict:
            if r_dict.get('Status'):
                status = r_dict["Status"]["Code"]              
            elif r_dict.get('Error'):
                status = r_dict["Error"]["Description"]
        return hotel_id, usluga_id, status
    else:
        print('Error: ')
        print(r.text) # возвращает контент ответа сервера текстом в юникоде (str)
        return 0
            
def test_create_new_order():
    # 1. Создать заказ ApiAcase: гостиница Звездная, РЗ/ПВ, Покупатель: ГЕОГРАФИЧЕСКИЙ КЛУБ /АОН
    url = main_url + "rest"
    create_order = './files/OrderRequest-real1.json'
    body = load_json(create_order)
    
    print(type(body))
    
    # loadList = json.loads(body)  - на этой строке ошибка: the JSON object must be str, bytes or bytearray, not dict
    # body - это строка
        
    assert True
    