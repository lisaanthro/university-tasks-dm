# 7.Бот-рецензии на фильмы:
# Кнопки: "Фильм дня", "Рекомендация по жанру", "Случайный фильм".
# Функции: Дает рекомендации на фильмы и их рецензии.

import telebot
from telebot import types
import json
import requests

from keys import TOKEN
from random import randint

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()
bot.set_webhook("https://functions.yandexcloud.net/d4enngkuek1a3j3s3gsf")

BUCKET_NAME = "movies-reviews-storage"

error_message = "Извините, фильм недоступен."


def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


def get_movies(filename):
    url = f"https://storage.yandexcloud.net/{BUCKET_NAME}/{filename}"
    response = requests.get(url)
    return response.json()


@bot.message_handler(commands=['start'])
def greetings(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button1 = types.KeyboardButton('Фильм дня')
    button2 = types.KeyboardButton('Рекомендация по жанру')
    button3 = types.KeyboardButton('Случайный фильм')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Выберите один из вариантов: ', reply_markup=markup)


@bot.message_handler(regexp='Фильм дня')
def movie_of_the_day(message):
    movies_json = get_movies('movie_of_the_day.json')
    print(movies_json)
    movie_id = randint(0, len(movies_json))
    movie = movies_json.get(str(movie_id), 'Фильм дня недоступен')
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Рекомендация по жанру')
def movie_by_genre(message):
    genres_json = get_movies('movie_by_genre.json')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*list(genres_json.keys()))
    bot.send_message(message.chat.id, 'Выберите жанр:', reply_markup=markup)


@bot.message_handler(regexp='Комедия')
def comedy(message):
    movie = get_movies('movie_by_genre.json').get('Комедия', error_message)
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Драма')
def drama(message):
    movie = get_movies('movie_by_genre.json').get('Драма', error_message)
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Аниме')
def drama(message):
    movie = get_movies('movie_by_genre.json').get('Аниме', error_message)
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Романтика')
def drama(message):
    movie = get_movies('movie_by_genre.json').get('Романтика', error_message)
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Триллер')
def drama(message):
    movie = get_movies('movie_by_genre.json').get('Триллер', error_message)
    bot.send_message(message.chat.id, movie)


@bot.message_handler(regexp='Случайный фильм')
def movie_of_the_day(message):
    movies_json = get_movies('movie_of_the_day.json')
    print(movies_json)
    movie_id = randint(0, len(movies_json))
    movie = movies_json.get(str(movie_id), 'Фильм дня недоступен')
    bot.send_message(message.chat.id, movie)


# bot.polling(none_stop=True)
