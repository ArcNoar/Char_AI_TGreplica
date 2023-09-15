from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext


from tgbot.misc.states import CharacterState
from tgbot.services.openAI_Connnector import OpenAI_Connector
from tgbot.services.Amplitude_Connector import Amplitude_Logger

from tgbot.models.mainDB import setUserCharacterChoice, getCharacter, getCharacterChatLogWithUser, addToChatLog
#Maybe i will do cancel handler later.

async def character_choice(event : types.Message): # Techinically it's not message, but it's same so ok.
    userChoice = event.web_app_data.data

    #print(f'USER - CHOICE : {userChoice}') #Amplitude request here

    loadout_data = {
        "event_type" : 'webApp-user-choice',
        "user_id" : event.from_user.id,
        "choosen-character" : userChoice
    }

    await Amplitude_Logger(loadout_data)

    setUserCharacterChoice(str(event.from_user.id), userChoice) # saving user choice.

    # (optional) create MW check that will pre load user choice for next session.

    character_data = getCharacter(userChoice)

    
    await CharacterState.initial.set()
    await event.answer(character_data['greet_message'])

    


async def character_greet(message: types.Message, state: FSMContext, middleware_data):
    
    # get current choice from middleware.
    character_data = getCharacter(middleware_data['character_choice_id'])
    
    user_response = message.text
    user_chat_history = getCharacterChatLogWithUser(
        character=character_data['character_name'],
        user= str(message.from_user.id))  



    # Send request to OPEN AI.
    #print('USER request to OPEN AI') # change to amplitude.

    loadout_data = {
        "event_type" : 'user-OAI-request',
        "user_id" : message.from_user.id,
    }

    await Amplitude_Logger(loadout_data)

    try:
        character_response = await OpenAI_Connector(
            user_text=user_response, 
            character=character_data, 
            chat_history=user_chat_history)
        
        loadout_data = {
            "event_type" : 'character-OAI-response',
            "user_id" : message.from_user.id
        }

        print(character_response)
        await Amplitude_Logger(loadout_data)

    except Exception as _ex:
        print('[CHARACTER HANDLER : Request to OAI] : ', _ex)

    character_answer = character_response['choices'][0]['message']['content']

    try:

        await message.answer(character_answer)

        loadout_data = {
            "event_type" : 'character-TG-answer',
            "user_id" : message.from_user.id
        }

        await Amplitude_Logger(loadout_data)
    except Exception as _ex:
        print('[CHARACTER HANDLER : Sending answer to user] : ', _ex)

    # Saving

    addToChatLog(
        user_response,
        character_answer,
        middleware_data['character_choice_id'],
        str(message.from_user.id)
        )
    


def register_character(dp: Dispatcher):
    dp.register_message_handler(character_choice, content_types='web_app_data', state="*")
    dp.register_message_handler(character_greet, state=CharacterState.initial)