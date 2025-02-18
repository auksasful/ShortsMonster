from openai import OpenAI
from groq import Groq

# from modules.base import Pinterest


class GroqUtils():
    def __init__(self, api_key, text_model_whitelist=["llama-3.3-70b-versatile", "llama-3.3-70b-specdec", "llama3-70b-8192", "llama3-8b-8192", "llama-3.1-8b-instant"]):
        # self.api_url = api_url
        self.api_key = api_key
        self.text_model_whitelist = text_model_whitelist
        self.current_model_id = 0


    def get_best_model(self):
        return self.text_model_whitelist[self.current_model_id]
    
    def update_current_model_id(self):
        self.current_model_id += 1
        if self.current_model_id >= len(self.text_model_whitelist):
            self.current_model_id = 0

        
