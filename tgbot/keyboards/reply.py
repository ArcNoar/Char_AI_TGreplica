from aiogram.types import KeyboardButton , ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

main_RKB = [
    [KeyboardButton(text='Choose Character.', web_app=WebAppInfo(url='https://arcnoar.github.io/')),]
]

main = ReplyKeyboardMarkup(keyboard=main_RKB,
                           resize_keyboard=True,
                           input_field_placeholder="Click the button.")
