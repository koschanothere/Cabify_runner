import schedule
import time
import requests
import uuid


def get_weather_data_for_lat_and_lon(latitude, longitude, time_now=0):
    if time_now == 0:
        time_now = time.time()
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude}%2C{longitude}/{time_now}?unitGroup=metric&key=F2UCDSWDKXTX6AZB5JM2QGLTR&contentType=json'
    r = requests.get(url)
    data = r.json()
    
    days = [day['conditions'] for day in data['days'][0:7]]
    conditions = data['currentConditions']['conditions']
    
    result = {
        'days': days,
        'currentConditions': {
            'conditions': conditions
        }
    }
    return result 

# тут скрипт взятия данных о погоде каждый день - АНАЛИТИКА(?)