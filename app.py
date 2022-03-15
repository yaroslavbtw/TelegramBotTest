import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
from database import *

app = Flask(__name__)


def get_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def send_message(chat_id, text):
    method = 'sendMessage'
    token = get_env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{token}/{method}'
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def send_message_button(chat_id, text):
    method = 'sendMessage'
    token = get_env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{token}/{method}'
    data = {"chat_id": chat_id, "text": text, 'reply_markup': json.dumps({"keyboard": [
        [
            {"text": "Да"}
        ],
        [
            {"text": "Нет"}
        ]
    ],
        "resize_keyboard": True
    })}
    requests.post(url, data=data)


def mailing():
    cur = get_cursor()
    cur.execute(f"SELECT * FROM `users`;")
    for user in cur.fetchall():
        send_message(user[2], 'Привет, друзья')


def print_questions(chat_id):
    with open('questions', 'r') as f:
        for line in f:
            send_message(chat_id, line)


def start_poll():
    num = find_number_of_question(request.json['message']['chat']['id'])
    if num == 0:
        send_message(request.json['message']['chat']['id'],
                     'Тест начат! Для получения результата необходимо ответить на 58 вопросов. Чтобы остановить тест пропишите - /stopquest')
    else:
        pass


def stop_poll():
    pass


@app.route('/', methods=["POST"])
def process():
    print(request.json)
    if 'message' in request.json:
        check_user_in_db(request.json['message']['chat']['id'], request.json['message']['chat']['first_name'])
        if request.json['message']['text'] == '/mailing' and request.json['message']['chat']['id'] == int(get_env('CREATOR_CHAT_ID')):
            mailing()
        elif request.json['message']['text'] == '/startquest':
            start_poll()
        elif request.json['message']['text'] == '/stopquest':
            if check_status(request.json['message']['chat']['id']) is False:
                send_message(request.json['message']['chat']['id'], "Начни тест для начала, даун)")
        close_db()
    return {"ok": True}


if __name__ == '__main__':
    app.run()
