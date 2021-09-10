import requests


def print_hi(name):
    response = requests.post('https://zeapi.yandex.net/lab/api/yalm/text3', params={
        'filter': 1,
        'intro': 0,
        'query': 'Я хочу сказать тебе'
    })
    print(response.text)

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)