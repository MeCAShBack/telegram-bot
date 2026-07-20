import requests
@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id,"city" , parse_mode='HTML')
    bot.register_next_step_handler(message, weather)
def get_weather(message):
    city = message.text.lower().strip()
    res = requests.get("")
    data = res.json()
    if data["cod"] == 200:
        temp = data["main"]["temp"]
        feel = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        caption =(
            f"weather cost{city}:\n"
            f"temp: {description}\n"
            f"humidity: {humidity}\n"
            f"wind_speed: {wind_speed}\n"
            f"wind_deg: {wind_deg}\n"
            f"feel: {feel}\n"

        )
        file = open("weather.txt", "a")
        bot.send_photo(message.chat.id,file ,
        caption=caption)
    else:
        bot.reply_to (message , "city not found:")
        bot.register_next_step_handler(message, get_weather)
    bot.register_next_step_handler(message, weather)




