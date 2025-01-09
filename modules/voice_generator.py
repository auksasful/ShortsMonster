import os
import re
from modules.base_generator import BaseGenerator
from openai import OpenAI
from modules.nagaac_utils import NagaACUtils


class VoiceGenerator(BaseGenerator):
    def __init__(self, project_folder, api_key, api_url="https://api.naga.ac/v1", voice_model_whitelist=['default-eleven-monolingual-v1', 'default-eleven-turbo-v2', 'default-eleven-multilingual-v1', 'default-eleven-multilingual-v2']):
        # Call the constructor of the base class
        super().__init__(project_folder)

        self.client = OpenAI(base_url=api_url,api_key=api_key)

        self.nagaac_utils = NagaACUtils(api_key, api_url=api_url, text_model_whitelist=[], image_model_whitelist=[], voice_model_whitelist=voice_model_whitelist)



    def read_json_data(self):
        return self.read_json(self.script_videos_file_path)


    def execute(self, video_id, scene, prompt, voice):
        save_path = os.path.join(self.generated_images, str(video_id), self.remove_symbols(scene))
        os.makedirs(save_path, exist_ok=True)

        response = self.generate_voice_nagaac(prompt, voice=voice)
        # print(response)
        # save the audio file
        file_name = os.path.join(save_path, "voiceover.mp3")
        with open(file_name, "wb") as f:
            f.write(response.content)

    def generate_voice_nagaac(self, prompt, voice, system_prompt=''):
        current_model_id = self.nagaac_utils.get_best_model(image_model=False, voice_model=True)
        print(current_model_id)
        rate_limit_cheked = False
        rate_limit_exceeded = False
        while not rate_limit_cheked:
            try:
                response = self.client.audio.speech.create(model=current_model_id,
                                            input=prompt,
                                            voice=voice,
                                            speed=1)
                rate_limit_exceeded = False
                self.nagaac_utils.update_api_usage(current_model_id, exceeded=rate_limit_exceeded, voice_model=True)
            except Exception as e:
                print(e)
                if 'rate_limit_exceeded' or 'Invalid model' or 'no_sources_available' or 'Input should be' in str(e):
                    rate_limit_exceeded = True
                    self.nagaac_utils.update_api_usage(current_model_id, exceeded=rate_limit_exceeded, voice_model=True)
                    current_model_id = self.nagaac_utils.get_best_model(image_model=False, voice_model=True)
            rate_limit_cheked = not rate_limit_exceeded
        return response

    @staticmethod
    def remove_symbols(text): 
        # Replace non-space symbols with an empty string 
        return re.sub(r'[^\w\s]', '', text)
