from modules.script_writer import ScriptWriter
from modules.script_divider import ScriptDivider
from modules.prompts_writer import PromptsWriter
from modules.image_generator import ImageGenerator
from modules.footage_downloader import FootageDownloader
from modules.voice_generator import VoiceGenerator
from modules.video_generator import VideoGenerator

def run_script_writer(project_folder):
    writer = ScriptWriter(project_folder)
    writer.execute()

def run_script_divider(project_folder):
    divider = ScriptDivider(project_folder)
    divider.execute()

def run_prompts_writer(project_folder):
    prompts = PromptsWriter(project_folder)
    prompts.execute()

def run_image_generator(project_folder):
    generator = ImageGenerator(project_folder)
    generator.execute()

def run_footage_downloader(project_folder):
    downloader = FootageDownloader(project_folder)
    downloader.execute()

def run_voice_generator(project_folder):
    voice = VoiceGenerator(project_folder)
    voice.execute()

def run_video_generator(project_folder):
    video = VideoGenerator(project_folder)
    video.execute()

def run_full_pipeline(project_folder):
    run_script_writer(project_folder)
    run_script_divider(project_folder)
    run_prompts_writer(project_folder)
    run_image_generator(project_folder)
    run_footage_downloader(project_folder)
    run_voice_generator(project_folder)
    run_video_generator(project_folder)

def main():
    project_folder = 'Weight loss'

    print(
        "Select a mode of operation:\n"
        "1. Script generation (ScriptWriter)\n"
        "2. Script division into scenes (ScriptDivider)\n"
        "3. Prompts generation (PromptsWriter)\n"
        "4. Image generation (ImageGenerator)\n"
        "5. Video footage download (FootageDownloader)\n"
        "6. Voiceover generation (VoiceGenerator)\n"
        "7. Video generation (VideoGenerator)\n"
        "8. Full process (Full Pipeline)\n"
    )

    choice = input("Enter the number corresponding to the mode: ")

    if choice == "1":
        run_script_writer(project_folder)
    elif choice == "2":
        run_script_divider(project_folder)
    elif choice == "3":
        run_prompts_writer(project_folder)
    elif choice == "4":
        run_image_generator(project_folder)
    elif choice == "5":
        run_footage_downloader(project_folder)
    elif choice == "6":
        run_voice_generator(project_folder)
    elif choice == "7":
        run_video_generator(project_folder)
    elif choice == "8":
        run_full_pipeline(project_folder)
    else:
        print("Invalid input, please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()