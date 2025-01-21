import os

from openai import OpenAI
# from g4f.client import Client
import os
import re
import sqlite3
import requests


from modules.base_generator import BaseGenerator
from modules.writer.writer import Writer


class ScriptWriter(BaseGenerator):
    def __init__(self, project_folder, api_key, gemini_api_key, text_model_whitelist=["default-gemini-1.5-pro", "default-gpt-3.5-turbo"], api_url="https://api.naga.ac/v1"):
        super().__init__(project_folder)
        self.writer = Writer(api_key=api_key, gemini_api_key=gemini_api_key, text_model_whitelist=text_model_whitelist, api_url=api_url)

    def execute(self, prompt):
        response = self.writer.generate_text_nagaac(prompt)
        response = self.writer.structure_script_gemini(response)
        file_path = self.script_file_path
        self.write_csv(file_path, response)

