
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from tgbot.config import load_config

from tgbot.models.mainDB import getUserByID, registerNewUser
from tgbot.services.Amplitude_Connector import Amplitude_Logger

config = load_config()



class Entry_Middleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        print('NEW Update')
        #print('Pre-Process Update Stage')
        #data['middleware_data'] = "Some data for on_post_process_update"
    
        if update.message:
            user = update.message.from_user

        elif update.callback_query:
            user = update.callback_query.from_user

        else:
            return
        
        userIn_DB = getUserByID(str(user.id)) # Lookin up for user in DB

        # Ideally we should store recent users, so we can check it without calling out DB everytime.

        if userIn_DB == False: 
            
            loadout_data = {
                "event_type" : "new-user",
                "user_id" : str(user.id)
            }

            await Amplitude_Logger(exported_data=loadout_data)
            registerNewUser(
                user_id=str(user.id),
                username=user.username,
                firstname=user.first_name,
                lastname=user.last_name
            )
        else: # userIn_DB contains user data pulled from db, but for now i'll ignore that
            print('Its Existing User.')

            # loadout_data = {
            #     "event_type" : "message-from-user",
            #     "user_id" : str(user.id)
            # }

            #await Amplitude_Logger(exported_data=loadout_data)


    async def on_process_message(self, message: types.Message, data: dict):
        # Pulling user data and storing it in handler middleware space
        data['middleware_data'] = getUserByID(str(message.from_user.id)) 