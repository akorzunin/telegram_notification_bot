import asyncio
import logging
import pickle
from aiogram import Bot

#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
operator = Bot(TOKEN)

async def send_message_to_user_by_id(user_id, message):
    await operator.send_message(user_id, message)

sub_user_list = (
    503131177,
)

async def send_message_():
    while 1:
        # do some calculations
        # get list of pairs
        # with open('rule_list.pkl', 'rb') as f:
        #     rule_list = pickle.load(f)
        # pair_list = [i.pair for i in rule_list]
        # # if calculations got any useful result send a message
        # for i in rule_list:
        #     await send_message_to_user_by_id(i.user_id, 'message')
        logging.info('pepe_pog')
        await asyncio.sleep(60)
