#from datetime import date
#import gspread
import os
import telebot
import logging
import psycopg2
from config import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
#googlesheet_id = 'https://docs.google.com/spreadsheets/d/1E-F6Nfm2iLEaVTN-4eh2b2uYfE10eZ_9sNDrUZsZpzY/edit#gid=0'
#gc = gspread.service_account(filename='my-project-19798-python-bot-53bb87dd46fb.json')

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")