import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

API_TOKEN = '1597801339:AAF8oRCIMduDhyAw39XdwU6aBjEnVraiflk'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class UserForm(StatesGroup):
    name = State()
    age = State()
    gender = State()


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Числа'))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Числа')
async def numbers(message: types.Message):
    await message.answer('Сколько чисел прислать?')


@dp.message_handler()
async def send_numbers(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
    except:
        await message.answer('Нужно число')
        return
    if count > 0:
        await asyncio.gather(*[message.answer(str(i)) for i in range(count)])
    else:
        for i in range(-count):
            await message.answer(str(i))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
