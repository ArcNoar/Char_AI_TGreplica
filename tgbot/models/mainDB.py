
"""

Create Accesors

"""
from tgbot.services.DB_Manager import DB_Executor

from datetime import datetime


def registerNewUser(user_id : str, username : str, firstname : str, lastname : str):

    """
    Creating data about new user, contains :
        user_id (primary key)
        username
        firstname
        lastname
        character_choice (Use SOMETHING to add choice)
        reg_data : datetime.now()

    """

    reg_data = str(datetime.now())


    queryLine = """ INSERT INTO public."iden_tg_users" 
                    (user_id,username,firstname,lastname, reg_data) VALUES """ + f"""
                    ('{user_id}', '{username}', '{firstname}', '{lastname}', '{reg_data}');"""

    DB_Executor(queryLine, "ADD")

def setUserCharacterChoice(user_id : str, character : str):
    """
    
    Saving user character choice in DB

    """

    query = f""" UPDATE public.iden_tg_users SET
                character_choice_id = '{character}'::character varying WHERE
                user_id = '{user_id}'; """
    
    DB_Executor(query, "EDIT")

def getUserByID(user_id: str):
    """
    
    return userData from db by ID
    {
        'user_id': str,
        'username': str,
        'firstname': str,
        'lastname': str,
        'character_choice_id': str,
        'reg_data': datetime.datetime(),
    }

    if not exist => False

    """
    
    select_query = f"""SELECT * FROM public."iden_tg_users" WHERE user_id = '{user_id}' ;"""

    pulled_data = DB_Executor(select_query, "GET")

    #print(pulled_data)

    if pulled_data != False :
        return {'user_id' : pulled_data[0],
                'username' : pulled_data[1],
                'firstname' : pulled_data[2],
                'lastname' : pulled_data[3],
                'reg_date' : str(pulled_data[4]),
                'character_choice_id' : pulled_data[5]}
    
    return pulled_data



def getCharacter(character : str):
    """
    
    return Character from db by his name
    {
        'character_name': str,
        'char_instructions': str,
        'greet_message': str,
    }

    if not exist => False

    """
    
    select_query = f"""SELECT * FROM public."iden_characters" WHERE character_name = '{character}' ;"""

    pulled_data = DB_Executor(select_query, "GET")

    #print(pulled_data)

    if pulled_data != False :
        return {'character_name' : pulled_data[0],
                'char_instructions' : pulled_data[1],
                'greet_message' : pulled_data[2],
                }
    
    return pulled_data


def addToChatLog(message, response, character, user_id):
    
    """
    Creating data about user interaction with character, contains :
        id [PK] (Creates automatically) 
        char_response
        user_response
        involved_character_id (character name)
        involved_used_id (user name)

    """

    filtered_response = response.replace("'",'"')
    #print(filtered_response)
    filtered_message = message.replace("'",'"')
    #print(filtered_message)

    queryLine = """ INSERT INTO public."iden_chat_log" 
                    (char_response,user_response,involved_character_id, involved_user_id) VALUES """ + f"""
                    ('{filtered_response}'::text, '{filtered_message}'::text, '{character}', '{user_id}') returning id; """

    DB_Executor(queryLine, "ADD")


# this is enough for now.
def getCharacterChatLogWithUser(character, user):
    """
    
    return Interaction from db by Character and User
    [
        {
            'id' : int,
            'char_response': str,
            'user_response': str,
            'involved_character_id': str,
            'involved_user_id' : str,
        },
        {
            id' : int,
            'char_response': str,
            'user_response': str,
            'involved_character_id': str,
            'involved_user_id' : str,
        },
    ]

    if not exist => False

    """
    
    select_query = f"""SELECT * FROM public."iden_chat_log" WHERE involved_character_id = '{character}' AND involved_user_id = '{user}';"""

    pulled_data = DB_Executor(select_query, "GETALL")

    transformed_data = []

    #print(pulled_data)

    if pulled_data != False :
        for batch in pulled_data:
            converted_data = {
                'id' : batch[0],
                'char_response' : batch[1],
                'user_response' : batch[2],
                'involved_character_id' : batch[3],
                'involved_user_id' : batch[4],
                }
            transformed_data.append(converted_data)

        return transformed_data
    
    return pulled_data