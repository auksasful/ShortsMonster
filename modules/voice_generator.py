import os
import re
from modules.base_generator import BaseGenerator
from openai import OpenAI
from modules.nagaac_utils import NagaACUtils


class VoiceGenerator(BaseGenerator):
    def __init__(self, project_folder, api_key, api_url="https://api.naga.ac/v1"):
        # Call the constructor of the base class
        super().__init__(project_folder)

        self.client = OpenAI(base_url=api_url,api_key=api_key)

        # TODO: Add the NagaACUtils class with voice models switching
        # self.nagaac_utils = NagaACUtils(api_key,text_model_whitelist=self.text_model_whitelist)



    def read_json_data(self):
        return self.read_json(self.script_videos_file_path)


    def execute(self, video_id, scene, prompt):
        save_path = os.path.join(self.generated_images, str(video_id), self.remove_symbols(scene))
        os.makedirs(save_path, exist_ok=True)

        # TODO: attempt to use models switching for faster response (in NagaACUtils class)
        models = ['eleven-monolingual-v1', 'eleven-turbo-v2', 'eleven-multilingual-v1', 'eleven-multilingual-v2']
        response = self.client.audio.speech.create(model=models[0],
                                            input=prompt,
                                            voice="George",
                                            speed=1)
        # print(response)
        # save the audio file
        file_name = os.path.join(save_path, "voiceover.mp3")
        with open(file_name, "wb") as f:
            f.write(response.content)


    @staticmethod
    def remove_symbols(text): 
        # Replace non-space symbols with an empty string 
        return re.sub(r'[^\w\s]', '', text)
