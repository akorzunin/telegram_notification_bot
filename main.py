
import asyncio
import uvicorn
from aiogram import Bot
import nest_asyncio
import logging

LOG_FILE_NAME = 'log_file_name.log'
format = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(
    filename=None, 
    format=format,
    encoding='utf-8', 
    level=logging.INFO, 
)

from modules.aiogram_modules import aiogram_app
from modules.aiogram_modules import message_handler
# from modules.api_modules import fast_api_app 
from modules.api_modules.uvicorn_config import CONFIG
from modules import poll_handler

def main():
    loop = asyncio.get_event_loop()
    # create fastapi task
    config = uvicorn.Config(**CONFIG, loop=loop)
    server = uvicorn.Server(config)
    loop.create_task(server.serve())

    # tasks
    loop.create_task(poll_handler.send_message_())

    # setup debug console to work w/ awaitables
    nest_asyncio.apply(loop) 

    message_handler.setup(aiogram_app.dp)
    aiogram_app.executor.start_polling(aiogram_app.dp, skip_updates=True)
    
if __name__ == '__main__':
    main()