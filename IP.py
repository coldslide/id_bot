import telebot
import requests
import datetime
import pytz  

TOKEN = 'TELEGRAM_TOKEN'
bot = telebot.TeleBot(TOKEN)

CHAT_ID = 'CHAT_ID'  

bot_runs = 0  

def get_location(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    return response.json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global bot_runs
    bot_runs += 1  

    server_ip = requests.get('https://api.ipify.org').text
    location_data = get_location(server_ip)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_utc = datetime.datetime.now(pytz.timezone('UTC')).astimezone()  

    response_message = (
        f"пользователь {message.from_user.first_name} запустил бота.\n"
        f"IP сервера: {server_ip}\n"
        f"дата и время запуска: {current_time}\n"
        f"время в UTC: {current_time_utc.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"количество запусков бота: {bot_runs}\n"
        f"User ID: {message.from_user.id}\n"
        f"Username: @{message.from_user.username if message.from_user.username else 'нет'}\n"
        f"геолокация: {location_data.get('city', 'неизвестно')}, "
        f"{location_data.get('region', 'неизвестно')}, "
        f"{location_data.get('country', 'неизвестно')}\n"
        f"широта: {location_data.get('loc', '').split(',')[0]}\n"
        f"долгота: {location_data.get('loc', '').split(',')[1]}\n"
        f"ISP: {location_data.get('org', 'неизвестно')}\n"
        f"организация: {location_data.get('hostname', 'неизвестно')}\n"
        f"язык пользователя: {message.from_user.language_code if message.from_user.language_code else 'неизвестно'}"
    )

    bot.send_message(CHAT_ID, response_message)
    bot.reply_to(message, "в списке тебя нету) приобрести ботов/программы и разные приколы можно тут: https://t.me/m/20yi1rVpMTcy")

bot.polling(none_stop=True)
