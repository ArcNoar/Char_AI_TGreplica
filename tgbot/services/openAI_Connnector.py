
from tgbot.config import load_config
import openai

import aiohttp
import json


config = load_config()

openai.api_key = config.misc.openAI_Token



async def OpenAI_Connector(user_text : str, character: dict, chat_history : list): # Make it class
    """

    returns response.json
    
    """
    current_user_response = {"role": "user", "content": user_text}

    messages = [
            {"role": "system", "content": character['char_instructions']},
            {'role': 'assistant', 'content' : character['greet_message']},
        ]
    
    if chat_history != False: # Loading chat history (Not optimised)
        #print('CHAT HISTORY:', chat_history)
        for interaction in chat_history:
            fitted_interaction = [
                {
                    "role" : 'user', 'content' : interaction['user_response']
                },
                 {
                     "role" : 'assistant', 'content' : interaction['char_response']
                 }]
            messages += fitted_interaction

    #print('UPDATE MESSAGES : ' , messages)

    messages.append(current_user_response)       

    endpoint = 'http://95.217.14.178:8080/candidates_openai/gpt'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            return await response.json()
        




