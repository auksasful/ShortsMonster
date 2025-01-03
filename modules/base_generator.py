import csv
import os
import re


class BaseGenerator:

    SCRIPT_FILE_NAME = 'script.csv'

    def __init__(self, project_folder):
        # Forming paths to the project directories
        self.project_folder = os.path.join('projects', project_folder)

        self.generated_images = os.path.join(self.project_folder, 'generated_images')
        self.generated_video = os.path.join(self.project_folder, 'generated_video')
        self.script_file_path = os.path.join(self.project_folder, self.SCRIPT_FILE_NAME)

        # Automatically create project folder and its subdirectories if they do not exist
        os.makedirs(self.generated_images, exist_ok=True)
        os.makedirs(self.generated_video, exist_ok=True)

    def read_csv(self, file_path):
        # Logic for reading a CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if file_path == self.script_file_path:
                    scenes = []
                    row_array = row[0].split('\n')
                    # print('row_array: ' + str(row_array))
                    header_met = False
                    new_scene_array = []
                    for row_ in row_array:

                        header = '"Scene" |^| "Duration" |^| "Text" |^| "Visuals" |^| "Hashtags" |^| "Description"'
                        if row_ == header:
                            header_met = True
                            continue
                        
                        if header_met and (row_.count('|^|') == 5):
                            # print('row_nested: ' + str(row_))
                            row_scene = row_.split('|^|')
                            # add dictionary to new_scene_array
                            duration_value = row_scene[1].strip()
                            duration_value = int(re.search(r'\d+', duration_value).group())

                            new_scene_array.append({
                                "Scene": row_scene[0],
                                "Duration": duration_value,
                                "Text": row_scene[2],
                                "Visuals": row_scene[3],
                                "Hashtags": row_scene[4],
                                "Description": row_scene[5]
                            })
                        else:
                            if header_met:
                                scenes.append(new_scene_array)
                                new_scene_array = []
                            header_met = False

                    
                    
                    return scenes
                    # script = []
                    # for row in reader:
                    #     scene_data = {
                    #         "Scene": int(row[0]),
                    #         "Duration": int(row[1]),
                    #         "Text": row[2],
                    #         "Visuals": row[3],
                    #         "Hashtags": row[4]
                    #     }
                    #     script.append(scene_data)
                    # return script
                    


    def write_csv(self, file_path, response):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([response])
    