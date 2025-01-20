from modules.writer.script_writer import ScriptWriter
from modules.script_divider import ScriptDivider
from modules.writer.prompts_writer import PromptsWriter
from modules.image_generator import ImageGenerator
from modules.footage_downloader import FootageDownloader
from modules.voice_generator import VoiceGenerator
from modules.video_generator import VideoGenerator
from config import Config
import random

from modules.writer.writer import Writer

prompts = [
    'Create a 30-second Tiktok video script about [5 easy healthy snacks for weight loss].\n'
    'Required format: csv file delimited by |^| with 5 columns: Scene, Duration, Text, Visuals, Hashtags, Description.\n'
    'Output the list of these columns.'
    'The duration should be integer.'
    'There MUST be lots of scenes that keep changing every 3 seconds.'
    """this is the example formatting:
    "Here is a 30-second TikTok video script about 5 easy healthy snacks for weight loss:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 3 |^| ""Hey everyone, welcome back to my channel. Today, I'm sharing 5 easy healthy snacks for weight loss."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthysnacks #weightloss"" |^| ""Introduction to the video""
""Snack 1: Fresh Fruits"" |^| 5 |^| ""First up, we have fresh fruits like apples, bananas, and oranges. They're rich in fiber and antioxidants."" |^| ""Footage of fresh fruits on a plate"" |^| ""#freshfruits #healthyhabits"" |^| ""Showcasing the first snack""
""Snack 2: Nuts and Seeds"" |^| 5 |^| ""Next, we have nuts and seeds like almonds, walnuts, and chia seeds. They're high in protein and healthy fats."" |^| ""Footage of nuts and seeds in a bowl"" |^| ""#nutsandseeds #snacking"" |^| ""Showcasing the second snack""
""Snack 3: Carrot Sticks with Hummus"" |^| 5 |^| ""Third, we have carrot sticks with hummus. It's a tasty and healthy combination."" |^| ""Footage of carrot sticks with hummus"" |^| ""#carrotsticks #hummus"" |^| ""Showcasing the third snack""
""Snack 4: Greek Yogurt"" |^| 5 |^| ""Fourth, we have Greek yogurt. It's high in protein and can help with weight loss."" |^| ""Footage of Greek yogurt in a cup"" |^| ""#greek yogurt #weightloss"" |^| ""Showcasing the fourth snack""
""Snack 5: Protein Smoothie"" |^| 5 |^| ""Last but not least, we have a protein smoothie made with spinach, banana, and almond milk."" |^| ""Footage of a protein smoothie in a glass"" |^| ""#proteinsmoothie #healthydrinks"" |^| ""Showcasing the fifth snack""
""Conclusion"" |^| 2 |^| ""Thanks for watching, don't forget to subscribe for more healthy tips and tricks."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthyliving #weightlossjourney"" |^| ""Conclusion of the video"" 

Note: The duration of each scene is in seconds and adds up to 30 seconds."
"Here is a 30-second Tiktok video script about the top 3 fat-burning cardio exercises in the required format:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 5 |^| ""Hey there, fitness fam! Let's burn some fat with the top 3 cardio exercises"" |^| ""Upbeat background music, host appearing on screen with a friendly smile"" |^| ""#fitness #cardio #weightloss"" |^| ""Introduction to the video and host""
""Exercise 1: Running"" |^| 8 |^| ""Coming in at number 3, we have running! Burn up to 800 calories per hour"" |^| ""Footage of people running outdoors or on a treadmill, with calorie burn graphics"" |^| ""#running #cardio #fatburn"" |^| ""Presentation of the first exercise""
""Exercise 2: Jumping Rope"" |^| 8 |^| ""At number 2, we have jumping rope! This intense workout burns up to 700 calories per hour"" |^| ""Footage of people jumping rope, with calorie burn graphics and fun animations"" |^| ""#jumpingrope #cardio #calorieburn"" |^| ""Presentation of the second exercise""
""Exercise 3: Burpees"" |^| 8 |^| ""And at number 1, we have burpees! This full-body exercise burns up to 900 calories per hour"" |^| ""Footage of people doing burpees, with calorie burn graphics and motivational text"" |^| ""#burpees #cardio #weightloss"" |^| ""Presentation of the third exercise""
""Conclusion"" |^| 1 |^| ""So, which one will you try first? Let me know in the comments!"" |^| ""Host appearing on screen with a friendly smile, and a call-to-action graphic"" |^| ""#fitnessmotivation #cardioexercises #weightlossjourney"" |^| ""Conclusion and call-to-action"""
'''Here is a 30-second TikTok video script about drinking water before meals for weight loss in the required format:

Scene |^| Duration |^| Text |^| Visuals |^| Hashtags |^| Description
Introduction |^| 5 |^| Hey friends, want to boost your weight loss journey? |^| A person holding a water bottle with a friendly smile |^| #weightloss #healthytips |^| Introduction to the topic
Problem statement |^| 5 |^| Did you know that sometimes our brain mistakes thirst for hunger? |^| An animation of a brain with a thought bubble |^| #weightlossmotivation #healthyliving |^| Explaining the problem
Solution |^| 10 |^| Drinking water before meals can help with weight loss and reduce cravings |^| A person drinking water before eating a meal |^| #waterbeforemeals #weightlosshacks |^| Presenting the solution
Benefits |^| 5 |^| It can also improve digestion and increase energy levels |^| An animation of a person with a happy stomach and energetic movements |^| #healthbenefits #weightlossjourney |^| Highlighting the benefits
Call to action |^| 5 |^| So, make sure to drink a glass of water before your next meal |^| A person holding a glass of water with a reminder on the screen |^| #weightlosschallenge #healthyhabits |^| Encouraging viewers to take action'''
,

    'Create a 30-second Tiktok video script about [Top 3 fat-burning cardio exercises].\n'
    'Required format: csv file delimited by |^| with 5 columns: Scene, Duration, Text, Visuals, Hashtags, Description.\n'
    'Output the list of these columns.'
    'The duration should be integer.'
    'There MUST be lots of scenes that keep changing every 3 seconds.'"""this is the example formatting:
    "Here is a 30-second TikTok video script about 5 easy healthy snacks for weight loss:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 3 |^| ""Hey everyone, welcome back to my channel. Today, I'm sharing 5 easy healthy snacks for weight loss."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthysnacks #weightloss"" |^| ""Introduction to the video""
""Snack 1: Fresh Fruits"" |^| 5 |^| ""First up, we have fresh fruits like apples, bananas, and oranges. They're rich in fiber and antioxidants."" |^| ""Footage of fresh fruits on a plate"" |^| ""#freshfruits #healthyhabits"" |^| ""Showcasing the first snack""
""Snack 2: Nuts and Seeds"" |^| 5 |^| ""Next, we have nuts and seeds like almonds, walnuts, and chia seeds. They're high in protein and healthy fats."" |^| ""Footage of nuts and seeds in a bowl"" |^| ""#nutsandseeds #snacking"" |^| ""Showcasing the second snack""
""Snack 3: Carrot Sticks with Hummus"" |^| 5 |^| ""Third, we have carrot sticks with hummus. It's a tasty and healthy combination."" |^| ""Footage of carrot sticks with hummus"" |^| ""#carrotsticks #hummus"" |^| ""Showcasing the third snack""
""Snack 4: Greek Yogurt"" |^| 5 |^| ""Fourth, we have Greek yogurt. It's high in protein and can help with weight loss."" |^| ""Footage of Greek yogurt in a cup"" |^| ""#greek yogurt #weightloss"" |^| ""Showcasing the fourth snack""
""Snack 5: Protein Smoothie"" |^| 5 |^| ""Last but not least, we have a protein smoothie made with spinach, banana, and almond milk."" |^| ""Footage of a protein smoothie in a glass"" |^| ""#proteinsmoothie #healthydrinks"" |^| ""Showcasing the fifth snack""
""Conclusion"" |^| 2 |^| ""Thanks for watching, don't forget to subscribe for more healthy tips and tricks."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthyliving #weightlossjourney"" |^| ""Conclusion of the video"" 

Note: The duration of each scene is in seconds and adds up to 30 seconds."
"Here is a 30-second Tiktok video script about the top 3 fat-burning cardio exercises in the required format:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 5 |^| ""Hey there, fitness fam! Let's burn some fat with the top 3 cardio exercises"" |^| ""Upbeat background music, host appearing on screen with a friendly smile"" |^| ""#fitness #cardio #weightloss"" |^| ""Introduction to the video and host""
""Exercise 1: Running"" |^| 8 |^| ""Coming in at number 3, we have running! Burn up to 800 calories per hour"" |^| ""Footage of people running outdoors or on a treadmill, with calorie burn graphics"" |^| ""#running #cardio #fatburn"" |^| ""Presentation of the first exercise""
""Exercise 2: Jumping Rope"" |^| 8 |^| ""At number 2, we have jumping rope! This intense workout burns up to 700 calories per hour"" |^| ""Footage of people jumping rope, with calorie burn graphics and fun animations"" |^| ""#jumpingrope #cardio #calorieburn"" |^| ""Presentation of the second exercise""
""Exercise 3: Burpees"" |^| 8 |^| ""And at number 1, we have burpees! This full-body exercise burns up to 900 calories per hour"" |^| ""Footage of people doing burpees, with calorie burn graphics and motivational text"" |^| ""#burpees #cardio #weightloss"" |^| ""Presentation of the third exercise""
""Conclusion"" |^| 1 |^| ""So, which one will you try first? Let me know in the comments!"" |^| ""Host appearing on screen with a friendly smile, and a call-to-action graphic"" |^| ""#fitnessmotivation #cardioexercises #weightlossjourney"" |^| ""Conclusion and call-to-action"""
'''Here is a 30-second TikTok video script about drinking water before meals for weight loss in the required format:

Scene |^| Duration |^| Text |^| Visuals |^| Hashtags |^| Description
Introduction |^| 5 |^| Hey friends, want to boost your weight loss journey? |^| A person holding a water bottle with a friendly smile |^| #weightloss #healthytips |^| Introduction to the topic
Problem statement |^| 5 |^| Did you know that sometimes our brain mistakes thirst for hunger? |^| An animation of a brain with a thought bubble |^| #weightlossmotivation #healthyliving |^| Explaining the problem
Solution |^| 10 |^| Drinking water before meals can help with weight loss and reduce cravings |^| A person drinking water before eating a meal |^| #waterbeforemeals #weightlosshacks |^| Presenting the solution
Benefits |^| 5 |^| It can also improve digestion and increase energy levels |^| An animation of a person with a happy stomach and energetic movements |^| #healthbenefits #weightlossjourney |^| Highlighting the benefits
Call to action |^| 5 |^| So, make sure to drink a glass of water before your next meal |^| A person holding a glass of water with a reminder on the screen |^| #weightlosschallenge #healthyhabits |^| Encouraging viewers to take action''',

    'Create a 30-second Tiktok video script about [Drinking water before meals for weight loss].\n'
    'Required format: csv file delimited by |^| with 5 columns: Scene, Duration, Text, Visuals, Hashtags, Description.\n'
    'Output the list of these columns.'
    'The duration should be integer.'
    'There MUST be lots of scenes that keep changing every 3 seconds.'"""this is the example formatting:
    "Here is a 30-second TikTok video script about 5 easy healthy snacks for weight loss:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 3 |^| ""Hey everyone, welcome back to my channel. Today, I'm sharing 5 easy healthy snacks for weight loss."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthysnacks #weightloss"" |^| ""Introduction to the video""
""Snack 1: Fresh Fruits"" |^| 5 |^| ""First up, we have fresh fruits like apples, bananas, and oranges. They're rich in fiber and antioxidants."" |^| ""Footage of fresh fruits on a plate"" |^| ""#freshfruits #healthyhabits"" |^| ""Showcasing the first snack""
""Snack 2: Nuts and Seeds"" |^| 5 |^| ""Next, we have nuts and seeds like almonds, walnuts, and chia seeds. They're high in protein and healthy fats."" |^| ""Footage of nuts and seeds in a bowl"" |^| ""#nutsandseeds #snacking"" |^| ""Showcasing the second snack""
""Snack 3: Carrot Sticks with Hummus"" |^| 5 |^| ""Third, we have carrot sticks with hummus. It's a tasty and healthy combination."" |^| ""Footage of carrot sticks with hummus"" |^| ""#carrotsticks #hummus"" |^| ""Showcasing the third snack""
""Snack 4: Greek Yogurt"" |^| 5 |^| ""Fourth, we have Greek yogurt. It's high in protein and can help with weight loss."" |^| ""Footage of Greek yogurt in a cup"" |^| ""#greek yogurt #weightloss"" |^| ""Showcasing the fourth snack""
""Snack 5: Protein Smoothie"" |^| 5 |^| ""Last but not least, we have a protein smoothie made with spinach, banana, and almond milk."" |^| ""Footage of a protein smoothie in a glass"" |^| ""#proteinsmoothie #healthydrinks"" |^| ""Showcasing the fifth snack""
""Conclusion"" |^| 2 |^| ""Thanks for watching, don't forget to subscribe for more healthy tips and tricks."" |^| ""Host appearing on screen with a friendly smile"" |^| ""#healthyliving #weightlossjourney"" |^| ""Conclusion of the video"" 

Note: The duration of each scene is in seconds and adds up to 30 seconds."
"Here is a 30-second Tiktok video script about the top 3 fat-burning cardio exercises in the required format:

""Scene"" |^| ""Duration"" |^| ""Text"" |^| ""Visuals"" |^| ""Hashtags"" |^| ""Description""
""Introduction"" |^| 5 |^| ""Hey there, fitness fam! Let's burn some fat with the top 3 cardio exercises"" |^| ""Upbeat background music, host appearing on screen with a friendly smile"" |^| ""#fitness #cardio #weightloss"" |^| ""Introduction to the video and host""
""Exercise 1: Running"" |^| 8 |^| ""Coming in at number 3, we have running! Burn up to 800 calories per hour"" |^| ""Footage of people running outdoors or on a treadmill, with calorie burn graphics"" |^| ""#running #cardio #fatburn"" |^| ""Presentation of the first exercise""
""Exercise 2: Jumping Rope"" |^| 8 |^| ""At number 2, we have jumping rope! This intense workout burns up to 700 calories per hour"" |^| ""Footage of people jumping rope, with calorie burn graphics and fun animations"" |^| ""#jumpingrope #cardio #calorieburn"" |^| ""Presentation of the second exercise""
""Exercise 3: Burpees"" |^| 8 |^| ""And at number 1, we have burpees! This full-body exercise burns up to 900 calories per hour"" |^| ""Footage of people doing burpees, with calorie burn graphics and motivational text"" |^| ""#burpees #cardio #weightloss"" |^| ""Presentation of the third exercise""
""Conclusion"" |^| 1 |^| ""So, which one will you try first? Let me know in the comments!"" |^| ""Host appearing on screen with a friendly smile, and a call-to-action graphic"" |^| ""#fitnessmotivation #cardioexercises #weightlossjourney"" |^| ""Conclusion and call-to-action"""
'''Here is a 30-second TikTok video script about drinking water before meals for weight loss in the required format:

Scene |^| Duration |^| Text |^| Visuals |^| Hashtags |^| Description
Introduction |^| 5 |^| Hey friends, want to boost your weight loss journey? |^| A person holding a water bottle with a friendly smile |^| #weightloss #healthytips |^| Introduction to the topic
Problem statement |^| 5 |^| Did you know that sometimes our brain mistakes thirst for hunger? |^| An animation of a brain with a thought bubble |^| #weightlossmotivation #healthyliving |^| Explaining the problem
Solution |^| 10 |^| Drinking water before meals can help with weight loss and reduce cravings |^| A person drinking water before eating a meal |^| #waterbeforemeals #weightlosshacks |^| Presenting the solution
Benefits |^| 5 |^| It can also improve digestion and increase energy levels |^| An animation of a person with a happy stomach and energetic movements |^| #healthbenefits #weightlossjourney |^| Highlighting the benefits
Call to action |^| 5 |^| So, make sure to drink a glass of water before your next meal |^| A person holding a glass of water with a reminder on the screen |^| #weightlosschallenge #healthyhabits |^| Encouraging viewers to take action''',
]

# TODO: use gemini api structured response instead of stupid text dividing methods

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
    # "default-gemini-1.5-flash",
    # "default-gemini-1.5-flash-002",
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
    # "default-gpt-3.5-turbo",
    # "default-gpt-3.5-turbo-0125",
    # "default-gpt-3.5-turbo-1106",
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
    # "default-mistral-7b-instruct",
    # "default-mixtral-8x7b-instruct"
]


def run_script_writer(project_folder):
    writer = ScriptWriter(project_folder, Config.NAGA_AC_API_KEY, text_model_whitelist=ai_text_models)

    for prompt in prompts:
        writer.execute(prompt)

def run_script_divider(project_folder):
    divider = ScriptDivider(project_folder)
    rows = divider.read_script_data()
    for row in rows:
        for row_inner in row:
            divider.execute(line=row_inner)
    divider.write_json_data()

def run_prompts_writer(project_folder, prompt_for_images):
    prompts = PromptsWriter(project_folder, Config.NAGA_AC_API_KEY, ai_text_models)
    json_data = prompts.read_json_data()
    for video in json_data:
        for scene in video['scenes']:
            prompt = prompt_for_images.replace('[scene]', scene['visuals'])
            prompts.execute(prompt=prompt, video_id=video['video'], scene=scene['scene'])
    
    prompts.write_json_data()

def run_image_generator(project_folder):
    generator = ImageGenerator(project_folder)
    json_data = generator.read_image_prompts_json()
    for video in json_data:
        for scene in video['scenes']:
            if scene == video['scenes'][0] or scene == video['scenes'][-1]:
                generation_chance = 1
            else:
                generation_chance = 0.3
            generator.execute(video_id=video['video'], scene=scene['scene'], prompt=scene['image_prompt'], generation_chance=generation_chance)
            
    generator.write_json_data()

def run_footage_downloader(project_folder, mode='video', orietation='portrait'):
    downloader = FootageDownloader(project_folder, Config.PEXELS_API_KEY)
    writer = Writer(Config.NAGA_AC_API_KEY, text_model_whitelist=ai_text_models)
    json_data = downloader.read_script_videos_json()
    image_paths_json = downloader.read_image_paths_json()
    for video in json_data:
        for scene in video['scenes']:
            image_paths = image_paths_json[video['video'] - 1]["scenes"]
            for path in image_paths:
                if scene['scene'] == path['scene']:
                    image_path = path['image_path']
                    google_image_path = path['google_image_path']
                    break

            prompt = f"For scene {scene['text']} write a keyword that i could use to search for a video footage for. Do not explain what you are doing, just write the keyword."
            
            if image_path and google_image_path:
                continue

            keyword = writer.generate_text_nagaac(prompt=prompt)

            if not google_image_path:
                image_file_path = downloader.execute(query=keyword, pages=1, per_page=1, mode='photo', orientation=orietation)
            else:
                image_file_path = google_image_path
            
            if not image_path:
                file_path = downloader.execute(query=keyword, pages=1, per_page=1, mode=mode, orientation=orietation)
            else:
                file_path = image_path
            downloader.update_image_path(video_id=video['video'], scene=scene['scene'], image_path=file_path, google_image_path=image_file_path)

def run_voice_generator(project_folder):
    available_voices = ['Aria', 'Roger', 'Sarah', 'Laura', 'Charlie', 'George', 'Callum', 'River', 'Liam', 'Charlotte', 'Alice', 'Matilda', 'Will', 'Jessica', 'Eric', 'Chris', 'Brian', 'Daniel', 'Lily', 'Bill']
    voice = VoiceGenerator(project_folder, Config.NAGA_AC_API_KEY)
    json_data = voice.read_json_data()
    for video in json_data:
        for scene in video['scenes']:
            voice.execute(video_id=video['video'], scene=scene['scene'], prompt=scene['text'], voice=available_voices[6])

def run_video_generator(project_folder):
    video_gen = VideoGenerator(project_folder)
    media_paths_json = video_gen.read_media_paths_json()
    script_videos_json = video_gen.read_script_videos_json()
    for video in script_videos_json:
        video_gen.execute(video_dict=video, media_paths_dict=media_paths_json[video['video'] - 1]["scenes"])

def run_full_pipeline(project_folder, prompt_for_images):
    run_script_writer(project_folder)
    run_script_divider(project_folder)
    run_prompts_writer(project_folder, prompt_for_images=prompt_for_images)
    run_image_generator(project_folder)
    run_footage_downloader(project_folder)
    run_voice_generator(project_folder)
    run_video_generator(project_folder)

def main():
    project_folder = 'Running'
    prompt_for_images='For scene [scene] write an image prompt. The goal is to generate very abstract visuals for this scene using this prompt that do not display any people or text. Do not explain what you are doing, just write the prompt.'

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
        run_prompts_writer(project_folder, prompt_for_images)
    elif choice == "4":
        run_image_generator(project_folder)
    elif choice == "5":
        run_footage_downloader(project_folder)
    elif choice == "6":
        run_voice_generator(project_folder)
    elif choice == "7":
        run_video_generator(project_folder)
    elif choice == "8":
        run_full_pipeline(project_folder, prompt_for_images)
    else:
        print("Invalid input, please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()