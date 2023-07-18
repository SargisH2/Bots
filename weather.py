import requests
import json
import telebot

with open('keys.txt', 'r') as f:
    weather_api_key=f.readline()
    telebot_info=f.readline()
bot = telebot.TeleBot(telebot_info)

def current_temp(city):
    response=requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no')
    if response.status_code!=200:
        return "Error. Status code: "+str(response.status_code)
    data_dict = json.loads(response.text)
    return f"{city}, {data_dict['location']['region']} region\nTime: {data_dict['location']['localtime']}\nTemperature: {data_dict['current']['temp_c']}C\nWind: {data_dict['current']['wind_kph']}kph"

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	weather_info=current_temp(message.text)
	# bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)
	bot.reply_to(message, weather_info)

bot.infinity_polling()