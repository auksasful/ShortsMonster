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
    
    def write_json_data(self):
        json_data = [{"video": video_id, **video_data} for video_id, video_data in self.videos.items()]
        self.write_json(self.script_videos_file_path, json_data)

    def execute(self, line):
        # print(f"row: {line}")
        if line == self.header:
            self.header_met = True
            self.current_video_id += 1
            self.videos[self.current_video_id] = {"scenes": []}
            return
        
        if self.header_met and (line.count('|^|') == 5):
            row_scene = line.split('|^|')
            # add dictionary to new_scene_array
            duration_value = row_scene[1].strip()
            duration_value = int(re.search(r'\d+', duration_value).group())
            scene_data = { 
                "scene": row_scene[0].strip().strip('"'), 
                "duration": duration_value, 
                "text": row_scene[2].strip().strip('"'),
                "visuals": row_scene[3].strip().strip('"'),
                "hashtags": row_scene[4].strip().strip('"'),
                "description": row_scene[5].strip().strip('"')
            } 
            self.videos[self.current_video_id]["scenes"].append(scene_data)
        else:
            self.header_met = False

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

        