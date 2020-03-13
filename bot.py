import telebot
import pyowm
import pyowm.exceptions
from secrets import *
import time	

bot = telebot.TeleBot(TELEG_TOKEN, threaded=False)
owm = pyowm.OWM(OWM_TOKEN)


def find_dot(msg):
	for i in msg:
		if '.' in i:
			return i


@bot.message_handler(commands=['start'])
def command_start(message):
	bot.send_message(message.chat.id, "The bot has started!\nEnter /help to see bot's functions")


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "☁ Current weather -  .place | Example:  	.London")


@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith('.') and not msg.text.endswith('.'))
def command_weather(message):	
	words = message.text.split()
	in_text = find_dot(words)
	if in_text == '.':
		pass
	else:
		parsed_msg = message.text.split('.')
	try:
		observation = owm.weather_at_place(str(parsed_msg[1]))
	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(message.chat.id, "Wrong place")

	weather = observation.get_weather()
	temperature = weather.get_temperature('celsius')["temp"]
	wind = weather.get_wind()['speed']
	clouds = weather.get_clouds()
	humidity = weather.get_humidity()
	answer = "🏙 In " + str(parsed_msg[1]) + " is currently " + weather.get_detailed_status() + "\n🌡️  " + str(temperature) + " °C" + "\n💨  " + str(wind) + " m/s" + "\n🌫️  " + str(clouds) + " %" + "\n💦  " + str(humidity) + " %"
	bot.send_message(message.chat.id, answer)


while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		time.sleep(1)
