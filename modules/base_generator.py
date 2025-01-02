import csv
import os


class BaseGenerator:
    def __init__(self, project_folder):
        # Forming paths to the project directories
        self.project_folder = os.path.join('projects', project_folder)

        self.generated_images = os.path.join(self.project_folder, 'generated_images')
        self.generated_video = os.path.join(self.project_folder, 'generated_video')

        # Automatically create project folder and its subdirectories if they do not exist
        os.makedirs(self.generated_images, exist_ok=True)
        os.makedirs(self.generated_video, exist_ok=True)

    def read_csv(self, file_name):
        # Logic for reading a CSV file
        pass

    def write_csv(self, file_path, response):
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([response])
    