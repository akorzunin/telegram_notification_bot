
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from telegram import MAX_MESSAGE_LENGTH

from modules import binance_api_handler as bah
from modules.utils.text_formatters import get_ticker_text
from modules.utils.util_functions import chunks

#load .env variables
import os
from dotenv import load_dotenv
import requests
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
MAX_MESSAGE_LENGTH = 4096
# API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """This handler will be called when user sends `/start` or `/help` command"""
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler(commands=['get_info'])
async def send_welcome(message: types.Message):
    '''Get info about user which send /get_info command'''
    text = f'''
        User info:
        Message id: {message.message_id}
        User name: {message.from_user.first_name} {message.from_user.last_name}
        Nickname: {message.from_user.username}
        User id: {message.from_user.id}
        Interfase language: {message.from_user.language_code}
        '''
    await message.answer(text)
    
@dp.message_handler(commands=['docs'])
async def docs(message: types.Message):
    host_ip = requests.get('https://api.ipify.org').content.decode('utf8')
    text = f'''
    Current host location: {host_ip}
    
    Link to docs page:
    http://{host_ip}:8000/docs
    '''

    await message.answer(text)
    
@dp.message_handler(commands=['get_ticker'])
async def get_ticker(message: types.Message):
    if arguments := message.get_args():
        pair = arguments.split(' ')[0]
        global bnc_client
        df = await bah.get_pair_ticker(
            pair=pair,
        )
        text = get_ticker_text(df)
        await message.answer(text)
    else:
        await message.answer('Enter a valid pair. Example: /get_ticker BTCUSDT')

@dp.message_handler(commands=['get_all_symbols'])
async def get_all_symbols(message: types.Message):
    text = await bah.get_all_pairs()
    if len(str(text)) >= MAX_MESSAGE_LENGTH:
        msg_chunk = chunks(text, int((MAX_MESSAGE_LENGTH-10)/12))
        for num, i in enumerate(msg_chunk):
            await message.answer(f'Page {num}\n{i}')
    else:
        await message.answer(text)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)