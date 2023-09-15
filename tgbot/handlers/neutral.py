from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_neutral(message: types.Message):
    text = [
        "Choose character to continue, using button, or following commands:",
        "/menu \n /start",
    ]

    await message.answer('\n'.join(text))


def register_neutral(dp: Dispatcher):
    dp.register_message_handler(bot_neutral)
