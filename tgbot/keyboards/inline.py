from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

#Not working

main_IKB = [
    [InlineKeyboardButton(text='Choose Character.', web_app=WebAppInfo(url='https://arcnoar.github.io/')),]
]

main = InlineKeyboardMarkup(keyboard=main_IKB)



