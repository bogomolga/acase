import requests
import json
import cx_Oracle
import pytest 

# Шаги:
# 1. Создать заказ ApiAcase: гостиница Звездная, РЗ/ПВ, Покупатель: ГЕОГРАФИЧЕСКИЙ КЛУБ /АОН
# 2. Получение информации о заказе
# 3. Бронирование по заказу ApiAcase
# 4. Проверка статуса заказа в БД

main_url = "http://10.0.0.129:8130/bora/"
json_headers = {
    "Content-type": "application/json",
    "Bora-Alien": "2"
}
connection = cx_Oracle.connect(user="BO_TEST_13", password="SYS", dsn="10.0.0.137:1521/test")



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
    create_order = './xml/OrderRequest-real1.json'
    body = load_json(create_order)
    loadList = json.loads(body)
    r = requests.post(url, headers=json_headers, json=loadList, verify=False) 
    print("Создать заказ ApiAcase. Ответ: ", r.text)
    id_ = getOrderId(r)  
    id_to_str = f'"{id_}"' # преобразование в str

    # 2. Получение информации о заказе                                      
    body = f'{{"OrderInfoRequest": {{"Id":{id_to_str}, "UserType":"INNER", "UserId":"after", "Password":"1", "Language":"ru", "ProfitCentreCode":"", "SUserCode":"", "MarketCode":"", "AgentCode":"", "BuyerCode":"", "UkCode":"", "CurrencyCode":"", "BuyerId": ""}}}}'
    loadList = json.loads(body)
    r = requests.get(url, headers=json_headers, json=loadList, verify=False)
    hotel_id, usluga_id, status = getOrderInfo(r)
    print(f"ID гостиницы: {hotel_id}, ID услуги: {usluga_id}, Статус: {status}")

    # 3. Бронирование по заказу ApiAcase
    url = main_url + "integration/ApiAcase"
    set_65 = './xml/ApiAcase_65.json'
    body = load_json(set_65)
    loadList = json.loads(body)
    r = requests.post(url, headers=json_headers, json=loadList, verify=False)
    #print("Бронирование ApiAcase. Ответ: ", r.text) 

    # 4. Проверка статуса заказа в БД
    with connection as db:
        with db.cursor() as cursor:
            sql = "select b_regnum, b_stat from ord_m where b_regnum = %s" % id_
            #print("DB query: ", sql)
            for r in cursor.execute(sql):
                print("DB result: ", r) # tuple object
            status = r[1]            
            print("Статус: ", status)
    
    assert status == 65
    