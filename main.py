from modules.script_writer import ScriptWriter
from modules.script_divider import ScriptDivider
from modules.prompts_writer import PromptsWriter
from modules.image_generator import ImageGenerator
from modules.footage_downloader import FootageDownloader
from modules.voice_generator import VoiceGenerator
from modules.video_generator import VideoGenerator
from config import Config

prompts = [
    'Create a 30-second Tiktok video script about [5 easy healthy snacks for weight loss].\n'
    'Required format: Python list of dictionaries. Split the script into scenes, then pack each scene into a dictionary. '
    'Output the list of these dictionaries.',

    'Create a 30-second Tiktok video script about [Top 3 fat-burning cardio exercises].\n'
    'Required format: Python list of dictionaries. Split the script into scenes, then pack each scene into a dictionary. '
    'Output the list of these dictionaries.',

    'Create a 30-second Tiktok video script about [Drinking water before meals for weight loss].\n'
    'Required format: Python list of dictionaries. Split the script into scenes, then pack each scene into a dictionary. '
    'Output the list of these dictionaries.'
]

def run_script_writer(project_folder):
    ai_text_models = [
        # "default-deepseek-chat",
        # "default-learnlm-1.5-pro-experimental",
        # "default-gemini-2.0-flash-thinking-exp",
        # "default-gemini-2.0-flash-thinking-exp-1219",
        # "default-gemini-2.0-flash-exp",
        # "default-gemini-exp",
        # "default-gemini-exp-1206",
        # "default-gemini-exp-1121",
        # "default-gemini-exp-1114",
        # "default-gemini-1.5-pro-exp",
        # "default-gemini-1.5-pro-exp-0801",
        # "default-gemini-1.5-pro",
        # "default-gemini-1.5-pro-002",
        "default-gemini-1.5-flash",
        "default-gemini-1.5-flash-002",
        # "default-grok-2",
        # "default-grok-2-1212",
        # "default-grok-2-vision",
        # "default-grok-2-vision-1212",
        # "default-grok-vision-beta",
        # "default-grok-beta",
        # "default-chatgpt-4o-latest",
        # "default-o1",
        # "default-o1-2024-12-17",
        # "default-o1-preview",
        # "default-o1-preview-2024-09-12",
        # "default-o1-mini",
        # "default-o1-mini-2024-09-12",
        # "default-gpt-4o",
        # "default-gpt-4o-2024-11-20",
        # "default-gpt-4o-2024-08-06",
        # "default-gpt-4o-2024-05-13",
        # "default-gpt-4o-mini",
        # "default-gpt-4o-mini-2024-07-18",
        # "default-gpt-4-turbo",
        # "default-gpt-4-turbo-2024-04-09",
        # "default-gpt-4-turbo-preview",
        # "default-gpt-4-0125-preview",
        # "default-gpt-4-1106-preview",
        # "default-gpt-4",
        # "default-gpt-4-0613",
        "default-llama-3.3-70b-instruct",
        "default-llama-3.2-90b-vision-instruct",
        "default-llama-3.2-11b-vision-instruct",
        "default-llama-3.2-3b-instruct",
        "default-llama-3.2-1b-instruct",
        "default-llama-3.1-405b-instruct",
        "default-llama-3.1-70b-instruct",
        "default-llama-3.1-8b-instruct",
        "default-llama-3-70b-instruct",
        "default-llama-3-8b-instruct",
        # "default-mixtral-8x22b-instruct",
        # "default-command-r-plus",
        # "default-command-r",
        # "default-mistral-large",
        # "default-mistral-large-2411",
        # "default-codestral",
        # "default-codestral-2405",
        "default-gpt-3.5-turbo",
        "default-gpt-3.5-turbo-0125",
        "default-gpt-3.5-turbo-1106",
        # "default-claude-3.5-sonnet",
        # "default-claude-3.5-sonnet-20241022",
        # "default-claude-3.5-haiku",
        # "default-claude-3.5-haiku-20241022",
        # "default-claude-3-opus",
        # "default-claude-3-opus-20240229",
        # "default-claude-3-sonnet",
        # "default-claude-3-sonnet-20240229",
        # "default-claude-3-haiku",
        # "default-claude-3-haiku-20240307",
        # "default-claude-2.1",
        # "default-claude-instant",
        # "default-gemini-pro",
        "default-llama-2-70b-chat",
        "default-llama-2-13b-chat",
        "default-llama-2-7b-chat",
        "default-mistral-7b-instruct",
        "default-mixtral-8x7b-instruct"
    ]
    writer = ScriptWriter(project_folder, Config.NAGA_AC_API_KEY, text_model_whitelist=ai_text_models)

    for prompt in prompts:
        writer.execute(prompt)

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