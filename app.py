import os
from flask import Flask, request
import telebot

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

#BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_TOKEN = '6332068214:AAES3Y1-pg27u6VUDY-VehyxrpgzcEsHa90'
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

app = Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    print("Received message")
    update_json = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    print("Setting webhook")
    bot.remove_webhook()
    bot.set_webhook(url=f'https://seveneleve.azurewebsites.net/{BOT_TOKEN}')
    return "!", 200

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print("Received message")
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print("Received message")
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    app.run(debug=True)
