import os
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
import yaml

from utils.loaders import PROMPTS
from config.settings import DEEPSEEK_API_KEY

class BernardoAssists:
    """
    Main class to interact with Bernardo, the personal assistant.
    It initializes the LLM and provides a method to send messages to Bernardo and receive responses.
    """

    def __init__(self):
        
        # initialize language model
        self.llm = self._initiailize_llm()

        # load system prompt from yaml file
        self.system_prompt = SystemMessage(content=PROMPTS["bernardo"]['system_instruction'])

    
    def _initiailize_llm(self):
        """
        Initialize the language model using the API key from environment variables.
        """
        api_key = DEEPSEEK_API_KEY

        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        return ChatOpenAI(
            model="deepseek-chat",
            temperature=0.3,
            api_key=api_key,
            base_url="https://api.deepseek.com",
            max_tokens=2048,
        )
    
    def response(self, user_message: str) -> str:
        """
        Send a message to Bernardo and receive a response.
        """
        try:
            messages = [
                self.system_prompt,
                HumanMessage(content=user_message)
            ]

            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")
            return PROMPTS["bernardo"]['error_message']



        