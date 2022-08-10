import asyncio
import logging
from typing import Optional
import os
import time
from pandas import DataFrame
from aiogram import Bot

from modules import binance_api_handler as bah
from modules.api_modules.db_api import models, schemas
from modules.api_modules.db_api import crud
from modules.utils.text_formatters import get_ticker_text
from modules.utils.util_classes import DBContextManager as DBConnect
from modules import rules_logic as rl
from binance.client import AsyncClient

# load .env variables
TOKEN = os.getenv("TOKEN")
DEBUG = bool(os.getenv("DEBUG", None))
operator = Bot(TOKEN)


async def send_message_to_user_by_id(user_id, message):
    await operator.send_message(user_id, message)


def parse_mailing_text(rule: models.Rules, df: DataFrame) -> str:
    if not df.lastPrice.values:
        return "Failed to read data from DataFrame"
    return f"""
    Rule has been trggered

    Rule id: {rule.id}
    TresholdType: {rule.TresholdType}
    Trigger value: {rule.value}
    Last price on {rule.pair.upper()} stock: {df.lastPrice.values[0]}
        
    Since rule is triggered it's gonna be deleted
    """


async def mailing_task(client: Optional[AsyncClient]):
    t_start = time.time()
    # get info about all pairs
    df = await bah.get_all_pair_ticker(client)

    # get all rules from DB
    with DBConnect() as db:
        for user in db.query(models.Users).all():
            for rule in user.rules:
                # check if rule is true or false
                if rl.check_rule(
                    treshold_type=rule.TresholdType,
                    trigger_value=rule.value,
                    # get current value from df w/ all pairs data
                    current_value=float(
                        df.loc[df["symbol"] == rule.pair.upper()].lastPrice.values[0]
                    ),
                ):
                    # send message to user.chat_id
                    text = parse_mailing_text(
                        rule=rule,
                        df=df.loc[df["symbol"] == rule.pair.upper()],
                    )
                    await send_message_to_user_by_id(
                        user_id=user.chat_id,
                        message=text,
                    )
                    # delete rule since it's triggered
                    if crud.delete_rule_by_id(db, rule.id):
                        logging.info(f"Rule {rule.id} triggered and deleted")
    logging.info(f"Mailng tsk done in {time.time() - t_start} s")


async def perpetual_coroutine():
    client = await bah.get_async_client()
    while 1:
        if not DEBUG:
            asyncio.gather(mailing_task(client))
            await asyncio.sleep(60)
        else:
            await mailing_task(client)
            await asyncio.sleep(2)
