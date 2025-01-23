import re
import json
from modules.base_generator import BaseGenerator
from collections import defaultdict


class ScriptDivider(BaseGenerator):
    def __init__(self, project_folder, append=False):
        # Call the constructor of the base class
        super().__init__(project_folder)
        self.header = '"Scene" |^| "Duration" |^| "Text" |^| "Visuals" |^| "Hashtags" |^| "Description"'
        self.header_met = False
        self.videos = self.initialize_videos(self.script_videos_file_path, append)
        self.current_video_id = len(self.videos)

    def read_script_data(self):
        data = self.read_csv(self.script_file_path)
        return data
    
    def execute(self, line):
        script_file_path = self.script_file_path


        with open(script_file_path, "r", encoding="utf-8") as f:
            old_json_strings = f.readlines()
            new_json_data = self.transform_data(old_json_strings)

        self.write_json(self.script_videos_file_path, new_json_data)

    @staticmethod
    def transform_data(old_json_strings):
        """
        Accepts a list of JSON strings in the old format
        and returns a list of dictionaries in the new format.
        """
        result = []
        for index, json_str in enumerate(old_json_strings, start=1):
            json_str = json_str.strip()
            if json_str.startswith('"') and json_str.endswith('"'):
                json_str = json_str[1:-1].replace('""', '"')
            old_data = json.loads(json_str)
    
            scene_objects = old_data.get("Scenes", [])
            
            scenes_list = []
            for i, s_obj in enumerate(scene_objects, start=1):
                scenes_list.append({
                    "scene": str(i),
                    "duration": 3,
                    "text": s_obj.get("What_Speaker_Says_In_First_Person", ""),
                    "visuals": s_obj.get("Visuals", ""),
                    "hashtags": old_data.get("Hashtags", ""),
                    "description": old_data.get("Description", "")
                })

            result.append({
                "video": index,
                "scenes": scenes_list
            })

        return result


    def initialize_videos(self, json_file_path, append):
        videos = defaultdict(lambda: {"scenes": []}) 
        if not append:
            return videos 
        # Load the initial videos data from a JSON file 
        initial_videos = self.read_json(json_file_path)
        # Convert the list to a defaultdict 
        for video in initial_videos: 
            video_id = video["video"] 
            videos[video_id]["scenes"] = video["scenes"] 
        return videos

        