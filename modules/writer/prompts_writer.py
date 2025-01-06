from modules.base_generator import BaseGenerator
from modules.writer.writer import Writer
from collections import defaultdict
import re
import json



class PromptsWriter(BaseGenerator):
    def __init__(self, project_folder, api_key, text_model_whitelist=["default-gemini-1.5-pro", "default-gpt-3.5-turbo"], api_url="https://api.naga.ac/v1"):
        super().__init__(project_folder)
        self.writer = Writer(api_key=api_key, text_model_whitelist=text_model_whitelist, api_url=api_url)
        self.videos = self.initialize_videos()


    def read_json_data(self):
        return self.read_json(self.script_videos_file_path)
    
    def write_json_data(self):
        json_data = [{"video": video_id, **video_data} for video_id, video_data in self.videos.items()]
        self.write_json(self.image_prompts_file_path, json_data)


    def execute(self, prompt, video_id, scene):
        response = self.writer.generate_text_nagaac(prompt)
        file_path = self.image_prompts_file_path

        scene_data = { 
            "scene": scene, 
            "image_prompt": response
        } 
        if "scenes" not in self.videos[video_id]:
            self.videos[video_id]["scenes"] = []
        self.videos[video_id]["scenes"].append(scene_data)


        self.write_json(file_path, self.videos)

    def initialize_videos(self):
        videos = defaultdict(lambda: {"scenes": []}) 
        return videos 