import csv
import os
import re
import json

class BaseGenerator:

    SCRIPT_FILE_NAME = 'script.csv'
    SCRIPT_VIDEOS_FILE_NAME = 'script_videos.json'
    IMAGE_PROMPTS_FILE_NAME = 'image_prompts.json'
    IMAGE_PATHS_FILE_NAME = 'image_paths.json'

    def __init__(self, project_folder):
        # Forming paths to the project directories
        self.project_folder = os.path.join('projects', project_folder)

        self.generated_images = os.path.join(self.project_folder, 'generated_images')
        self.generated_video = os.path.join(self.project_folder, 'generated_video')
        self.script_file_path = os.path.join(self.project_folder, self.SCRIPT_FILE_NAME)
        self.script_videos_file_path = os.path.join(self.project_folder, self.SCRIPT_VIDEOS_FILE_NAME)
        self.image_prompts_file_path = os.path.join(self.project_folder, self.IMAGE_PROMPTS_FILE_NAME)
        self.image_paths_file_path = os.path.join(self.project_folder, self.IMAGE_PATHS_FILE_NAME)

        # Automatically create project folder and its subdirectories if they do not exist
        os.makedirs(self.generated_images, exist_ok=True)
        os.makedirs(self.generated_video, exist_ok=True)

    def read_csv(self, file_path):
        # Logic for reading a CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            row_array = []
            for row in reader:
                if file_path == self.script_file_path:
                    row_array.append(row[0].split('\n'))
            if file_path == self.script_file_path:
                return row_array
                
    def write_csv(self, file_path, response):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([response])

    def write_json(self, file_path, response):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(response, file, indent=4)

    def read_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    