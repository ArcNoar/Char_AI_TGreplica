
import psycopg2

from tgbot.config import load_config


def DB_Executor(query : str, action: str):
    """
    
    Connecting and executing QUERY.

    action : ADD | GET | DEL | EDIT

    """
    config = load_config()

    try:
        #connection 
        connection = psycopg2.connect(
            host=config.db.host,
            user=config.db.user,
            password=config.db.password,
            database=config.db.database,

        )

        # Cursor action

        cursor = connection.cursor()
        
        cursor.execute(query)

        if action.upper() == "ADD":
            print('[DB-Executor] : ADD')
            connection.commit()

        elif action.upper() == "GET":
            print('[DB-Executor] : GET')
            pulled_data = cursor.fetchone()

            if pulled_data is None: # Data doesn't exist
                return False
            
            return pulled_data
        
        elif action.upper() == "GETALL":
            print('[DB-Executor] : GETALL')
            pulled_data = cursor.fetchall()

            if pulled_data is None: # Data doesn't exist
                return False
            
            return pulled_data

        elif action.upper() == "DEL":
            print('[DB-Executor] : DEL')

        elif action.upper() == "EDIT": # Basically same as ADD, but it's better to separate it.
            print('[DB-Executor] : EDIT')
            connection.commit()

        else:
            raise Exception('[DB-Executor] : wrong action parameter')
        
    
    except Exception as _ex:
        print(f"ERROR - {_ex}")
    finally:
        if connection:
            connection.close()
            print("[INFO] DB Connection Closed")

    
