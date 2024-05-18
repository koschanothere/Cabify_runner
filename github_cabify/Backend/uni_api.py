import pymongo
import requests
import json
import ymaps

# Подключение к базе данных MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")

db = client.taxi_prices

# Коллекции базы данных
districts_collection = db.storage
taxi_prices_collection = db.taxi_prices

# Получение всех районов Москвы
def get_districts():
    result = districts_collection.find({})
    return [district["features"][0:246]["properties"]["NAME"] for district in result]

# Поиск района по точке
def find_district(point):
    result = districts_collection.find({
        "type": "Polygon",
        "coordinates": [point]
    })
    return result[2]

# Получение цены такси по API Яндекс.Такси
def get_taxi_price_from_api(from_district, to_district):
    time_with_jams = ymaps.getJamsTime()
    length = ymaps.getLength()
    api_key = "790aa23d-7c53-410b-bfe0-c2ff5b0cd7fc"
    url = f"https://api-maps.yandex.ru/2.1/?lang=ru_RU&amp;coordorder=longlat&amp;apikey={api_key}"
    body = {
        "from": from_district,
        "to": to_district,
        "tariff": "economy",
    }
    response = requests.post(url, json=body)
    data = response.json()
    price = data["total"]
    return price

# Вставка цены такси в базу данных
def insert_taxi_price(from_district, to_district, price):
    taxi_prices_collection.insert_one({
        "from_district": from_district,
        "to_district": to_district,
        "price": price
    })

# Скрипт для запроса цен на такси по всем районам Москвы
def get_taxi_prices_for_all_districts():
    districts = get_districts()
    for from_district in districts:
        for to_district in districts:
            if from_district != to_district:
                point = {
                    "type": "Polygon",
                    "coordinates": [point]
                }
                district = find_district(point)
                from_district = district["features"][0:246]["properties"]["NAME"]
                price = get_taxi_price_from_api(from_district, to_district)
                insert_taxi_price(from_district, to_district, price)

get_taxi_prices_for_all_districts()


# Координаты точек маршрута
points = [[37.9271659429, 55.7487291122], [37.943649, 55.799156]]

# Запрос к API Яндекс.Такси для получения стоимости такси
headers = {'Content-Type': 'application/json'}
data = json.dumps({
    'route': points,
    'skip_estimated_waiting': True,
    'supports_forced_surge': False
})
response = requests.post('https://taxi.yandex.ru/3.0/routestats', headers=headers, data=data)

# Обработка ответа API
if response.status_code == 200:
    data = response.json()
    cost = data['cost']
    print(f'Стоимость такси: {cost} рублей')
else:
    print('Ошибка при запросе к API Яндекс.Такси')
