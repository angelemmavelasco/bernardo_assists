import psycopg2
import json
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from config.settings import (
    db_host,
    db_port,
    db_name,
    db_user,
    db_password,
    INSERT_MESSAGE_QUERY,
    GET_HISTORY_QUERY
)

class MemoryManager:
    """
    Class to manage memory interactions with the PostgreSQL database.
    """

    def __init__(self):
        self.conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
        )

        self.conn.autocommit =  True

    def save_message(self,*,
                     session_id:str = None,
                     role:str=None,
                     content:str=None,
                     ):
        """
        Save a message to the database. The message can be from the user or from Bernardo.
        """
        if not all([session_id, role, content]):
            print("Missing required parameters to save message")
            return

        message_data = {
            'type': role,
            'data':{'content': content}
        }

        query = INSERT_MESSAGE_QUERY

        try:

            with self.conn.cursor() as cursor:

                cursor.execute(query, (session_id, json.dumps(message_data)))

        except Exception as e:
            print(f"An error occurred while saving the message: {e}")

        return
    
    def get_history(self, *,
                    session_id:str = None,
                    limit:int = 15
                    ) -> list:
        
        """
        Retrieve the last 'limit' messages for a given session.
        Returns a list of LangChain message objects.
        """

        if not session_id:
            return []
        query = GET_HISTORY_QUERY

        try:
            with self.conn.cursor() as cursor:

                cursor.execute(query, (session_id, limit))

                rows = cursor.fetchall()

        except Exception as e:
            print(f"An error occurred while retrieving the message history: {e}")
            return []
        
        langchain_messages = []

        for row in reversed(rows):
            msg_dict = row[0] # psycopg2 ya convierte el JSONB a diccionario de Python automáticamente
            
            msg_type = msg_dict.get("type")
            msg_content = msg_dict.get("data", {}).get("content", "")
            
            if msg_type == "human":
                langchain_messages.append(HumanMessage(content=msg_content))
            elif msg_type == "ai":
                langchain_messages.append(AIMessage(content=msg_content))
                
        return langchain_messages
        