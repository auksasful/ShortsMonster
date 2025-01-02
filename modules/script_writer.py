import os

from openai import OpenAI
# from g4f.client import Client
import os
import re
import sqlite3
from openai import OpenAI
import requests


from modules.base_generator import BaseGenerator
from modules.nagaac_utils import NagaACUtils


class ScriptWriter(BaseGenerator):
    def __init__(self, project_folder, api_key, text_model_whitelist=["default-gemini-1.5-pro", "default-gpt-3.5-turbo"], api_url="https://api.naga.ac/v1"):
        # Call the constructor of the base class
        super().__init__(project_folder)

        self.text_model_whitelist = text_model_whitelist
        self.api_url = api_url

        self.client = OpenAI(base_url=self.api_url,api_key=api_key)

        self.nagaac_utils = NagaACUtils(api_key,text_model_whitelist=self.text_model_whitelist)
    
    def generate_text_nagaac(self, prompt, system_prompt=''):
        # print('writing single prompt')
        # print('before get best text model')
        current_model_id = self.nagaac_utils.get_best_model()
        print(current_model_id)
        rate_limit_cheked = False
        rate_limit_exceeded = False
        response_msg = ''
        while not rate_limit_cheked:
            try:
                response = self.client.chat.completions.create(
                model= current_model_id,
                messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': prompt}]
                )
                response_msg = response.choices[0].message.content
                rate_limit_exceeded = False
                self.nagaac_utils.update_api_usage(current_model_id, exceeded=rate_limit_exceeded)
            except Exception as e:
                print(e)
                if 'rate_limit_exceeded' or 'Invalid model' or 'no_sources_available' or 'Input should be' in str(e):
                    rate_limit_exceeded = True
                    self.nagaac_utils.update_api_usage(current_model_id, exceeded=rate_limit_exceeded)
                    current_model_id = self.nagaac_utils.get_best_model()
            rate_limit_cheked = not rate_limit_exceeded
        return response_msg

    def execute(self, prompt):

        response = self.generate_text_nagaac(prompt)


        file_path = os.path.join(self.project_folder, 'script.csv')

        self.write_csv(file_path, response)

