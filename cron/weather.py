#!/usr/bin/python

import json, urllib2, datetime
from sqlite3 import dbapi2 as sqlite3

# zip codes to log
zipcodes = ['07740','11210','33139','90210']

# configuration
DATABASE = '../db/weather.db'
SECRET_KEY = 'hackerati'
DEBUG = True

# open database
db = sqlite3.connect(DATABASE)

for zipcode in zipcodes:
    # pull weather from API
    weather_api = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us')
    weather_data = weather_api.read()
    weather_api.close()
    weather = json.loads(weather_data)

    # convert from kelvin to fahrenheit
    temp_val = (((weather['main']['temp']-273.15)*9)/5)+32
    humidity_val = weather['main']['humidity']
    print zipcode,
    print temp_val,
    print humidity_val

    # insert db entry
    db.execute('insert into weather (zipcode, temp, humidity, stamp) values (?, ?, ?, ?)',
                 [zipcode, int(temp_val), int(humidity_val), datetime.datetime.utcnow()])
    db.commit()

# close database
db.close()
