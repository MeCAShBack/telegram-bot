import telebot
import requests
from telebot import types
from currency_converter import CurrencyConverter
bot = telebot.TeleBot("8785518185:AAFntd8GrcqS8oUmZaBL-pX35U-5KvY1h5I")
API = "7a9ddc019331b2a2bf9020cd4eb5f777"
coin = CurrencyConverter()
@bot.message_handler(commands=["start"])
def send_start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("my creator")
    markup.row(btn1)
    btn2 = types.KeyboardButton("playlist")
    markup.row(btn2)
    bnt3 = types.KeyboardButton("🌤weather")
    markup.row(bnt3)
    btn4 = types.KeyboardButton("/currency")
    markup.row(btn4)
    bot.send_message(message.chat.id , f"hello!" , reply_markup=markup)

    file = open("handshake.jpg", "rb")
    bot.send_photo(message.chat.id, file)
@bot.message_handler(func=lambda message: message.text == "my creator")
def handle_creator(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💁‍♂️ Instagram", url="https://www.instagram.com/boucheron04/")
    markup.row(btn)
    bot.send_message(message.chat.id, "my creator", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "playlist")
def handle_playlist(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🎵 playlist", url="https://open.spotify.com/collection/tracks")
    markup.row(btn)
    bot.send_message(message.chat.id, "playlist", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🌤weather")
def handle_weather(message):
    bot.send_message(message.chat.id, "Write the city:")
    bot.register_next_step_handler(message, get_weather)
@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id , "city:", parse_mode="HTML")
    bot.register_next_step_handler(message, get_weather)
def get_weather(message):
    city = message.text.lower().strip()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    data = res.json()
    if data["cod"] == 200:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        caption =(
            f"🌤 Погода в {city}:\n"
            f"🌡 Температура: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"📋 Описание: {description}"
        )
        file = open("good weather.jpg" , "rb")
        bot.send_photo(
            message.chat.id,
            file,
            caption=caption,
        )
    else:
        bot.reply_to(message,"❌ Город не найден, попробуй ещё раз")
        bot.register_next_step_handler(message, get_weather)

@bot.message_handler(commands=["currency"])
def currency(message):
    bot.send_message(message.chat.id , "currency" , parse_mode="HTML")
    bot.register_next_step_handler(message, get_amount)

def get_amount(message):
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.reply_to(message, "❌ Введите число!")
        bot.register_next_step_handler(message, get_amount)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("USD → EUR", callback_data=f"USD_EUR_{amount}")
        btn2 = types.InlineKeyboardButton("EUR → USD", callback_data=f"EUR_USD_{amount}")
        btn3 = types.InlineKeyboardButton("USD → KGS", callback_data=f"USD_KGS_{amount}")
        btn4 = types.InlineKeyboardButton("EUR → KGS" , callback_data=f"EUR_KSG_{amount}")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id , "число должен быть больше 0.впешите сумму")
        bot.register_next_step_handler(message, get_amount)
@bot.callback_query_handler(func=lambda call: "_" in call.data)
def convert_currency(call):
    parts = call.data.split("_")
    from_currency = parts[0]
    to_currency = parts[1]
    amount = float(parts[2])
    try:
        result = coin.convert(amount,from_currency,to_currency)
        bot.send_message(
            call.message.chat.id,
            f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )
    except:
        bot.send_message(call.message.chat.id, "❌ Ошибка конвертации")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message.chat.id , "wassup")
@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id , "<u><b>About me</b></u>", parse_mode="HTML")
@bot.message_handler()
def info(message):
    if message.text.lower() =="hello":
        bot.send_message(message.chat.id, f"hello!{message.from_user.first_name}")
    elif message.text.lower() =="id":
        bot.reply_to(message, f"ID:{message.from_user.id}")

bot.infinity_polling()