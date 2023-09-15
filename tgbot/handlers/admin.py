from aiogram import Dispatcher
from aiogram.types import Message

# No need in this Handler but we will stay with it for a while

async def admin_start(message: Message):
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
