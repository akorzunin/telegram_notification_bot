
from typing import Optional
from fastapi import FastAPI

from modules.api_modules import util_routes
from modules.api_modules import db_routes
from modules import binance_api_handler as bah
from modules.aiogram_modules.aiogram_message_interface import send_message_to_user_by_id
from modules.api_modules.metadata import tags_metadata
from modules.utils.text_formatters import get_ticker_text

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(
    router=util_routes.router,
    tags=["Util"],
)
app.include_router(
    router=db_routes.router,
    prefix="/db",
    tags=["Database"],
)

# init client
@app.on_event("startup")
async def startup():
    # TODO can i make it w/o global???
    global bnc_client 
    bnc_client = await bah.get_async_client()

@app.on_event("shutdown")
async def shutdown():
    await bnc_client.close_connection()

@app.get("/get_pair_ticker", tags=["Manual"])
async def get_pair_ticker(pair: str):
    # call binance api for df
    df = await bah.get_pair_ticker(
        client=bnc_client,
        pair=pair,
    )
    return df.to_json(orient='records')

@app.get("/get_all_pairs", tags=["Manual"])
async def get_all_pairs():
    # call binance api for df
    symbols = await bah.get_all_pairs(
        client=bnc_client,
    )
    return symbols

@app.get("/send_pair_ticker_to_user", tags=["Aiogram"])
async def send_pair_ticker_to_user(user_id: int, pair: str):
    # call binance api for df
    df = await bah.get_pair_ticker(
        client=bnc_client,
        pair=pair,
    )
    # since \ cannot be used in f strings
    new_line = '\n' 
    text = get_ticker_text(df)
    # send df to user in telegram message
    await send_message_to_user_by_id(
        user_id=user_id,
        message=text,
    )
    return df.to_json(orient='records')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'fast_api_app:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        loop='asyncio'
    )