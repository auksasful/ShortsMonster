from openai import OpenAI
from modules.nagaac_utils import NagaACUtils
from modules.script_entity import Scene, Videos
import google.generativeai as genai
import json


class Writer:
    def __init__(self, api_key, gemini_api_key, text_model_whitelist=["default-gemini-1.5-pro", "default-gpt-3.5-turbo"], api_url="https://api.naga.ac/v1"):
        self.text_model_whitelist = text_model_whitelist
        self.api_url = api_url
        self.gemini_api_key = gemini_api_key

        self.client = OpenAI(base_url=self.api_url,api_key=api_key)

        self.nagaac_utils = NagaACUtils(api_key,text_model_whitelist=self.text_model_whitelist)


    def generate_text_nagaac(self, prompt, system_prompt=''):
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
    

    
    def structure_script_gemini(self, prompt):
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash') #, system_instruction=system_prompt)
        prompt = f"""
        Get text from the script based on the schema given. 

        {prompt}"""
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "response_schema": Videos})
       
        try:
            # Attempt to parse the response text as JSON
            json.loads(response.text)
            # If successful, print the formatted JSON
            # print(json.dumps(data, indent=4))
        except json.JSONDecodeError as e:
            # If parsing fails, print the error and the raw response text
            print(f"Error decoding JSON: {e}")
            print(f"Raw response text: {response.text}")
        # self.write_json(response.text, self.DATA_LIST_FILE_PATH, page)
        return response.text

    