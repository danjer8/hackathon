import os
import requests
from flask import Flask, request
import telebot
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = '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'

BOT_TOKEN = '6332068214:AAES3Y1-pg27u6VUDY-VehyxrpgzcEsHa90'
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

app = Flask(__name__)

def ask_gpt(prompt):
    """Send a prompt to the GPT model and return the response."""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',  # or another model name
        'prompt': prompt,
        'max_tokens': 150
    }
    response = requests.post('https://api.openai.com/v1/engines/gpt-3.5-turbo/completions', headers=headers, json=data)
    response_json = response.json()
    return response_json.get('choices', [{}])[0].get('text', '').strip()

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
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print("Received message")
    gpt_response = ask_gpt(message.text)
    bot.reply_to(message, gpt_response)

if __name__ == "__main__":
    app.run(debug=True)
