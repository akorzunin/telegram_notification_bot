import asyncio
import logging
import pickle
from typing import Optional
import requests
import os
from pandas import DataFrame
from aiogram import Bot
from fastapi import Depends
from modules import binance_api_handler as bah
from modules.api_modules.db_api import models, schemas
from modules.api_modules.db_api import crud
from modules.utils.text_formatters import get_ticker_text
from modules.utils.util_classes import DBContextManager as DBConnect
from modules import rules_logic as rl
from binance.client import AsyncClient
#load .env variables
TOKEN = os.getenv('TOKEN')
operator = Bot(TOKEN)

async def send_message_to_user_by_id(user_id, message):
    await operator.send_message(user_id, message)

def parse_mailing_text(rule: models.Rules, df: DataFrame) -> str:
    return f'''
    Rule has been trggered

    Rule id: {rule.id}
    TresholdType: {rule.TresholdType}
    Trigger value: {rule.value}
    Last price on {rule.pair} stock: {df.lastPrice.values[0]}
        
    Since rule is triggered it's gonna be deleted
    '''

async def mailing_task(client: Optional[AsyncClient]):
    # get info about all pairs
    df = await bah.get_all_pair_ticker(client)
    
    # get all rules from DB
    with DBConnect() as db:
        # rules = crud.read_all_rules(db)
        for user in db.query(models.Users).all():
            for rule in user.rules:
                # check if rule is true or false
                if (rl.check_rule(
                    treshold_type=rule.TresholdType,
                    trigger_value=rule.value,
                    #get current value from df w/ all pairs data
                    current_value=float(
                        df.loc[df['symbol'] == rule.pair].lastPrice.values[0]
                    )
                )):
                    # send message to user.chat_id
                    text = parse_mailing_text(
                        rule=rule, 
                        df=df.loc[df['symbol'] == rule.pair],
                    )
                    await send_message_to_user_by_id(
                        user_id=user.chat_id, 
                        message=text,
                    )
                    # delete rule since it's triggered
                    if crud.delete_rule_by_id(db, rule.id):
                        logging.info(f'Rule {rule.id} triggered and deleted')
                
async def perpetual_coroutine():
    client = await bah.get_async_client()
    while 1:
        # run logic for mailing other usres
        try:
            await mailing_task(client)
            await asyncio.sleep(60)
        except requests.exceptions.ConnectionError as e:
            logging.error(f'ConnectionError {e}')
