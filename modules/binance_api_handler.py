from pandas import DataFrame
import pandas as pd
import asyncio
from binance.client import Client, AsyncClient
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

async def get_pair_ticker(client: AsyncClient, pair: str) -> DataFrame:
    data = await client.get_ticker(
        symbol=pair,
    )
    df = pd.DataFrame(data, index=[0])
    unwanted = ['firstId', 'lastId', 'count', 'lastQty', 'bidQty', 'askQty']
    item_list = [e for e in list(df.keys()) if e not in unwanted]
    df = df[item_list]
    return df

def get_client():
    return Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

async def get_async_client():
    return await AsyncClient.create(BINANCE_API_KEY, BINANCE_SECRET_KEY)

async def create_async_client():
    return AsyncClient.create(BINANCE_API_KEY, BINANCE_SECRET_KEY)

async def main() -> None:
    client = await get_async_client() 
    df = await get_pair_ticker(client, 'RVNUSDT')
    print(df)
    await client.close_connection()

if __name__ == '__main__':

    # get RVNUSDT pair for example
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())