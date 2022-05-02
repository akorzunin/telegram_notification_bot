
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types

from modules import binance_api_handler as bah
from modules.utils.text_formatters import get_rules_text, get_ticker_text
from modules.utils.util_functions import chunks
from modules.utils.util_classes import DBContextManager as DBConnect, TresholdType
from modules.api_modules.db_api import crud, models, schemas

#load .env variables
import os
from dotenv import load_dotenv
import requests
load_dotenv()
API_TOKEN = os.getenv('TOKEN')
PORT=os.getenv('PORT', 8000)
MAX_MESSAGE_LENGTH = 4096
# API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """This handler will be called when user sends `/start` or `/help` command"""
    await message.answer('''
    Bot commands:

    start - initiate bot functions for user
    help - display availble commands
    get_info - get information about user
    docs - get link to docs api
    get_ticker - get information about trade pair [args: pair]
    new_rule - create rule that send notification if it's condition is true [args: pair, tresholdtype, value]
    get_all_symbols - get all info availble abou all pairs
    list_rules - get list of currently active rules for curren user
    del_rule - delete rule from user [args: rule_id]
    ''')

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
    http://{host_ip}:{PORT}/docs
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

@dp.message_handler(commands=['new_rule'])
async def new_rule(message: types.Message):
    if arguments := message.get_args():
        try:
            pair, treshold_type, value = arguments.split(' ')
        except ValueError:
            arguments = 0
        if arguments:    
            with DBConnect() as db:
                # crud.read_user_by_chat_id(db, chat_id)
                user_id = db.query(models.Users).filter_by(chat_id=message.chat.id).first().id
                item = schemas.RuleCreate(
                    owner_id=user_id,
                    pair=pair,
                    value=value,
                    TresholdType=TresholdType(treshold_type),
                )
                # create rule function
                a = crud.create_rule(db=db, item=item, )
                logging.info(f'Rule created {a}')
                text = f'Rule created'
                await message.answer(text)
    if not arguments:
        await message.answer(
            '''Enter a valid command. 
            Examples: 
            /new_rule RVNUSDT lower 1
            /new_rule BTCUSDT higher 1
            '''
        )

@dp.message_handler(commands=['get_all_symbols'])
async def get_all_symbols(message: types.Message):
    text = await bah.get_all_pairs()
    if len(str(text)) >= MAX_MESSAGE_LENGTH:
        msg_chunk = chunks(text, int((MAX_MESSAGE_LENGTH-10)/12))
        for num, i in enumerate(msg_chunk):
            await message.answer(f'Page {num}\n{i}')
    else:
        await message.answer(text)

@dp.message_handler(commands=['list_rules'])
async def list_rules(message: types.Message):
    with DBConnect() as db:
        user = db.query(models.Users).filter_by(chat_id=message.chat.id).first()
        db_user = crud.read_user_rules(db, user.id)
        rules_list=(
            schemas.RuleRead.from_orm(rule) for rule in db_user.rules
        )
        text = get_rules_text(rules_list)
        # breakpoint()
    await message.answer(text)

@dp.message_handler(commands=['del_rule'])
async def del_rule(message: types.Message):
    if arguments := message.get_args():
        rule_id = int(arguments)
        with DBConnect() as db:
            if crud.delete_rule_by_id(db, rule_id):
                text = f'Rule {rule_id} deleted'
            else:
                text = f'Rule {rule_id} Not found'
            await message.answer(text)
    if not arguments:
        await message.answer('''
        Enter a valid command. 
            Examples: 
            /del_rule 1
        '''
        )

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with DBConnect() as db:
        item = schemas.UserCreate(
            username=message.chat.username if message.chat.username is not None \
            else message.chat.first_name+message.chat.last_name,
            chat_id=message.chat.id,
        )
        user = crud.create_user(db, item)
        if user is None:
            await message.answer('User already exists')
        else:
            await message.answer('User created')


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)