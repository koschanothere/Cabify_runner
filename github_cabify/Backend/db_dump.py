import weather_api as weather
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = MongoClient('localhost', 27017)
db = client.weather
collection = db.weather_db

def add_weather_info_in_db():
    latitude = 55.75
    longitude = 37.61
    result = weather.get_weather_data_for_lat_and_lon(latitude, longitude)

    collection.insert_one(result)

add_weather_info_in_db()

db = client.taxi_prices

# Коллекции базы данных
districts_collection = db.storage
taxi_prices_collection = db.taxi_prices


# Получение всех районов Москвы
def get_districts():
    result = districts_collection.find({})
    return [district["properties"]["name"] for district in result]

# Поиск района по точке. ПОСМОТРЕТЬ. СДЕЛАТЬ (только на работу сайта, не аналитику)
def find_district(point):
    result = districts_collection.find({
        "geometry": {
            "$geoWithin": {
                "$geometry": point
            }
        }
    })
    return result[0]

# Вставка цены такси в базу данных
def insert_taxi_price(from_district, to_district, price):
    taxi_prices_collection.insert_one({
        "from_district": from_district,
        "to_district": to_district,
        "price": price
    })
