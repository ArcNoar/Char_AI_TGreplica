from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards import reply as KBR
#from tgbot.keyboards import inline as IKB #Not working

async def user_start(message: Message):
    await message.reply("Hello, user! It's Replicant. TG bot with GPT spice.")

    await message.answer('Click button to open WebApp where you can choose personalities to talk with. \n (Might not load properly on mobile ¯\_(ツ)_/¯)',
                         reply_markup=KBR.main)
    

async def user_menu(message: Message):

    await message.answer('Choose your character. \n (Might not load properly on mobile ¯\_(ツ)_/¯)',
                         reply_markup=KBR.main)

def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_menu, commands=["menu"], state="*")
