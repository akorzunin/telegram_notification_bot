
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types


# import callback_handler

#load .env variables
import os
from dotenv import load_dotenv
import requests
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
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
    http://{host_ip}:8001/docs
    '''

    await message.answer(text)

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)