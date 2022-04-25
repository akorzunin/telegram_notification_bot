import aiogram
from aiogram import Bot, Dispatcher, executor, types

async def pepe_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await message.answer('pepe!')

# @dp.message_handler(commands=['pepe',])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("pepe")

def setup(dp: Dispatcher):
    dp.register_message_handler(
        pepe_command, 
        commands=['pepe'],
        content_types=['text'], 
        state='*'
    )