# -*- coding: utf-8 -*-
import time
from datetime import datetime as dt, timedelta
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import requests, json
from imageGoogle import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def time_converter(time):
    converted_time = dt.fromtimestamp(
        int(time)
    ).strftime('%H:%M')
    return converted_time

def time_delta(from_time, d):
    return (dt.strptime(from_time, '%H:%M') + timedelta(hours=d)).time().strftime('%H:%M')

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command.startswith('/weather'):
        city_name = command.split(' ',1)[1]
        print(city_name)
        # Python program to find current
        # weather details of any city
        # using openweathermap api

        # Enter your API key here
        api_key = "**Insert here API key**"

        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"


        # complete_url variable to store
        # complete url address
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang=it"

        # get method of requests module
        # return response object
        response = requests.get(complete_url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found

        if x["cod"] != "404":
            image_path = get_image_url(city_name)


            # store the value of "main"
            # key in variable y
            y = x["main"]
            w = x["wind"]
            k = x["sys"]
            j = x["coord"]
            h = x["timezone"]
            g = (h-3600)/3600


            current_lon = j["lon"]
            current_lat = j["lat"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidiy = y["humidity"]


            current_wind_speed = w["speed"]
            current_wind_degree = ""
            if "deg" in w:
                current_wind_degree = w["deg"]
                if current_wind_degree >= 0 and current_wind_degree <= 22.5 or current_wind_degree > 337.5:
                    current_wind_degree = str(" N")
                elif current_wind_degree > 22.5 and current_wind_degree <= 67.5:
                    current_wind_degree = str(" NE")
                elif current_wind_degree > 67.5 and current_wind_degree <= 112.5:
                    current_wind_degree = str(" E")
                elif current_wind_degree > 112.5 and current_wind_degree <= 157.5:
                    current_wind_degree = str(" SE")
                elif current_wind_degree > 157.5 and current_wind_degree <= 202.5:
                    current_wind_degree = str(" S")
                elif current_wind_degree > 202.5 and current_wind_degree <= 247.5:
                    current_wind_degree = str(" SO")
                elif current_wind_degree > 247.5 and current_wind_degree <= 292.5:
                    current_wind_degree = str(" O")
                elif current_wind_degree > 292.5 and current_wind_degree <= 337.5:
                    current_wind_degree = str(" NO")

            current_sunrise = k["sunrise"]
            sunrise = time_converter(current_sunrise)
            current_sunset = k["sunset"]
            sunset = time_converter(current_sunset)

            local_hour_sunrise = time_delta(sunrise,g)
            local_hour_sunset = time_delta(sunset,g)
            local_hour = time_delta(dt.now().strftime('%H:%M'),g)

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]
            city_name = city_name.upper()

            # print following values
            stringa = city_name + "\n• Temperatura = " + str(round(current_temperature-273.15, 1))+" °C"\
                      +"\n• Pressione Atmosferica = " + str(current_pressure)+" hPa"\
                      +"\n• Umidità = " + str(current_humidiy)+"%" \
                      +"\n• Velocità Vento = " + str(round(current_wind_speed*3.6, 1)) + " Km/h" + str(current_wind_degree)\
                      +"\n• Descrizione del Cielo = " + str(weather_description)\
                      +"\n• Alba = " + str(local_hour_sunrise) + " (ora italiana " + str(sunrise) + ")"\
                      +"\n• Tramonto = " + str(local_hour_sunset) + " (ora italiana " + str(sunset) + ")"\
                      +"\n• Ora Locale = " + str(local_hour)
            bot.sendMessage(chat_id, str(stringa))
            bot.sendPhoto(chat_id, photo=open(image_path, 'rb'))
            bot.sendLocation(chat_id, current_lat, current_lon)
            delete_photo()




        else:
            bot.sendMessage(chat_id, "Città Non Trovata")
            bot.sendDocument(chat_id, "https://tenor.com/view/gerryscotti-cadutalibera-insomnia-gif-12874972")


bot = telepot.Bot('**Insert here Telegram Bot key**')
MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)
