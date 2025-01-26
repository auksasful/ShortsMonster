import os
from config import Config
from modules.base_generator import BaseGenerator
import numpy as np
import random
from PIL import Image
import textwrap
from moviepy.editor import (
    AudioFileClip, ImageClip, VideoFileClip, 
    concatenate_videoclips, vfx, CompositeVideoClip,
    VideoClip, TextClip
)
import whisper_timestamped as whisper
import os
import google.generativeai as genai
genai.configure(api_key=Config.GEMINI_API_KEY)

class VideoGenerator(BaseGenerator):
    def __init__(self, project_folder):
        # Call the constructor of the base class
        super().__init__(project_folder)

    def read_media_paths_json(self):
        return self.read_json(self.image_paths_file_path)
    
    def read_script_videos_json(self):
        return self.read_json(self.script_videos_file_path)

    def execute(self, video_dict, media_paths_dict):
        clip_paths = []
        media_types = []

        for i, scene in enumerate(video_dict['scenes']):
            for path in media_paths_dict:
                if scene['scene'] == path['scene']:
                    if (path['image_path'] == "" or path['image_path'] == None):
                        media_path = path['google_image_path']
                    else:
                        media_path = path['image_path']
            
            scene_id = scene['scene']
            print(media_path, scene['text'], scene_id)
            voiceover_path = os.path.join(self.generated_images, str(video_dict['video']), self.remove_symbols(scene['scene']), "voiceover.mp3")
            print(voiceover_path)
            video_path = os.path.join(self.generated_video, str(video_dict['video']), self.remove_symbols(scene['scene']), "video.mp4")
            os.makedirs(os.path.dirname(video_path), exist_ok=True)

            if not os.path.exists(video_path):
                # Calculate the duration of the audio file using AudioFileClip
                audio_duration = 0
                if os.path.exists(voiceover_path):
                    audio_duration = self.get_audio_duration(voiceover_path)

                print(audio_duration)

                # Create a video clip with the image/video and audio
                if media_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    effects = [
                        self.zoom_in_effect,
                        self.zoom_out_effect, #only these effects work properly
                        # self.slide_left_to_right,
                        # self.slide_right_to_left,
                        # self.slide_top,
                        # self.slide_bottom,
                        # self.circular_motion
                    ]
                    chosen_effect = random.choice(effects)
                    image = Image.open(media_path)
                    image = self.scale_and_crop(image)
                    video_clip = chosen_effect(image, duration=audio_duration)
                else:
                    video_clip = self.create_video_clip(media_path, audio_duration)
                # Add the audio to the video clip
                if audio_duration > 0:
                    audio_clip = AudioFileClip(voiceover_path)
                    video_clip.audio = audio_clip
                
                # Add text overlay
                # Get transcribed text with timestamps
                ffmpeg_path = "C:\\ffmpeg\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"  # Adjust this path if needed
                ffprobe_path = "C:\\ffmpeg\\ffmpeg-7.1-essentials_build\\bin\\ffprobe.exe"  # Adjust this path if needed
                os.environ["FFMPEG_BINARY"] = ffmpeg_path
                os.environ["FFPROBE_BINARY"] = ffprobe_path
                transcribed_text = self.get_transcribed_text(voiceover_path)
                # Create text clips for each word
                text_clips = self.get_text_clips(transcribed_text, fontsize=90)
                # Create composite video with original clip and text overlays
                video_clip = CompositeVideoClip([video_clip] + text_clips)

                # Save the video clip
                video_clip.write_videofile(video_path, codec="libx264", fps=24)
                video_clip.close()
                audio_clip.close()

                if media_path.lower().endswith(('.mp4', '.mov', '.avi')):
                    media_types.append("video")
                else:
                    media_types.append("image")
            else:
                media_types.append("video")

            clip_paths.append(video_path)

        # Generate the final video from the video clips
        final_video_path = os.path.join(self.generated_video, str(video_dict['video']), "final_video.mp4")
        print(final_video_path)
        os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
        self.concatenate_video_clips(clip_paths, final_video_path)
        
        # Extract audio from final video
        audio_clip = AudioFileClip(final_video_path)
        mp3_path = os.path.join(os.path.dirname(final_video_path), "audio.mp3")
        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()

        # Get transcript
        transcript = self.get_audio_transcript(mp3_path)

        # Save transcript
        transcript_path = os.path.join(os.path.dirname(final_video_path), "transcript.txt")
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        return final_video_path
    
    def get_transcribed_text(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        audio = whisper.load_audio(filename)
        model = whisper.load_model("small", device="cpu")
        results = whisper.transcribe(model, audio, language="en")

        return results["segments"]

    def get_text_clips(self, text, fontsize):
        text_clips = []
        for segment in text:
            for word in segment["words"]:
                text_clips.append(
                    TextClip(word["text"],
                        fontsize=fontsize,
                        method='caption',
                        stroke_width=5, 
                        stroke_color="white", 
                        font="Arial-Bold",
                        color="white")
                    .set_start(word["start"])
                    .set_end(word["end"])   
                    .set_position("center")
                )
        return text_clips


    def get_audio_transcript(self, audio_path):
        # Initialize a Gemini model appropriate for your use case.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        audio_file = genai.upload_file(audio_path)

        # Create the prompt.
        prompt = """Generate a transcript of the speech with timestamps in seconds (numbers displayed). Each timestamped segment should contain no more than 2 words.
        Example format:
        00:00:00.000 --> 00:00:01.000 Hey everyone.

00:00:01.000 --> 00:00:02.000 Welcome back.

00:00:02.000 --> 00:00:03.000 Today, sharing.

00:00:03.000 --> 00:00:04.000 Five snacks.

00:00:04.000 --> 00:00:05.000 First up.

00:00:05.000 --> 00:00:06.000 Fresh fruits.

00:00:06.000 --> 00:00:07.000 Apples, bananas.

00:00:07.000 --> 00:00:08.000 Rich fiber.

00:00:08.000 --> 00:00:09.000 Next, nuts.

00:00:09.000 --> 00:00:10.000 Almonds, seeds.

00:00:10.000 --> 00:00:11.000 High protein.

00:00:11.000 --> 00:00:12.000 Third, carrots.

00:00:12.000 --> 00:00:13.000 With hummus.

00:00:13.000 --> 00:00:14.000 Tasty combo.

00:00:14.000 --> 00:00:15.000 Fourth, yogurt.

00:00:15.000 --> 00:00:16.000 Weight loss.

00:00:16.000 --> 00:00:17.000 Last, smoothie.

00:00:17.000 --> 00:00:18.000 Spinach, banana.

00:00:18.000 --> 00:00:19.000 Thanks, watching.

00:00:19.000 --> 00:00:20.000 Subscribe now.
        """

        # Pass the prompt and the audio file to Gemini.
        response = model.generate_content([prompt, audio_file])

        # return the transcript.
        return response.text  

    def get_audio_duration(self, audio_path):
        # Get the duration of the audio file
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        audio_clip.close()
        return duration
    
    def create_video_clip(self, media_path, audio_duration):
        # Create a video clip with the image/video and audio
        if media_path.lower().endswith(('.mp4', '.mov', '.avi')):
            video_clip = VideoFileClip(media_path).subclip(0, audio_duration)
            video_clip = video_clip.set_duration(audio_duration)
            return video_clip
        else:
            image_clip = ImageClip(media_path, duration=audio_duration)
            image_clip = image_clip.set_duration(audio_duration)
            return image_clip
        
    def concatenate_video_clips(self, clip_paths, final_video_path):
        # Concatenate the video clips
        video_clips = [VideoFileClip(clip_path).subclip(0, VideoFileClip(clip_path).duration - 0.1) for clip_path in clip_paths]
        
        # Resize all clips to the same size
        min_width = min(clip.size[0] for clip in video_clips)
        min_height = min(clip.size[1] for clip in video_clips)
        video_clips = [clip.resize(newsize=(min_width, min_height)) for clip in video_clips]
        
        # Use crossfadein
        padding = 0.15
        video_fx_list = [video_clips[0]]
        idx = video_clips[0].duration - padding
        for clip in video_clips[1:]:
            video_fx_list.append(clip.set_start(idx).crossfadein(padding))
            idx += clip.duration - padding

        final_video = CompositeVideoClip(video_fx_list)
        final_video.write_videofile(final_video_path, codec="libx264", fps=24)
        final_video.close()
        return final_video_path
    

    def scale_and_crop(self, image, scale_factor=1.2):
        w, h = image.size
        nw, nh = int(w * scale_factor), int(h * scale_factor)
        scaled_img = image.resize((nw, nh), Image.LANCZOS)
        left = (nw - w) // 2
        top = (nh - h) // 2
        # Keep a larger area to prevent black edges with sliding and circular effects
        cropped_img = scaled_img.crop((left, top, left + w, top + h))
        return cropped_img

    def zoom_in_effect(self, image, duration, zoom_factor=1.2):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            zoom = 1 + (zoom_factor - 1) * (t / duration)
            new_w, new_h = int(w * zoom), int(h * zoom)
            if new_w <= 0 or new_h <= 0:
                return img_np
            img_resized = Image.fromarray(img_np).resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - w) // 2
            top = (new_h - h) // 2
            return np.array(img_resized.crop((left, top, left + w, top + h)))

        return VideoClip(make_frame, duration=duration)

    def zoom_out_effect(self, image, duration, zoom_factor=1.5):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            zoom = zoom_factor - (zoom_factor - 1) * (t / duration)
            new_w, new_h = int(w * zoom), int(h * zoom)
            if new_w <= 0 or new_h <= 0:
                return img_np
            img_resized = Image.fromarray(img_np).resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - w) // 2
            top = (new_h - h) // 2
            return np.array(img_resized.crop((left, top, left + w, top + h)))

        return VideoClip(make_frame, duration=duration)

    def slide_left_to_right(self, image, duration, shift=40):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            offset = int(shift * (t / duration))
            frame = Image.new("RGB", (w, h), (0, 0, 0))
            frame.paste(Image.fromarray(img_np), (offset - shift, 0))
            return np.array(frame)

        return VideoClip(make_frame, duration=duration)

    def slide_right_to_left(self, image, duration, shift=40):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            offset = int(shift * (t / duration))
            frame = Image.new("RGB", (w, h), (0, 0, 0))
            frame.paste(Image.fromarray(img_np), (shift - offset, 0))
            return np.array(frame)

        return VideoClip(make_frame, duration=duration)

    def slide_top(self, image, duration, shift=40):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            offset = int(shift * (t / duration))
            frame = Image.new("RGB", (w, h), (0, 0, 0))
            frame.paste(Image.fromarray(img_np), (0, offset - shift))
            return np.array(frame)

        return VideoClip(make_frame, duration=duration)

    def slide_bottom(self, image, duration, shift=40):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            offset = int(shift * (t / duration))
            frame = Image.new("RGB", (w, h), (0, 0, 0))
            frame.paste(Image.fromarray(img_np), (0, shift - offset))
            return np.array(frame)

        return VideoClip(make_frame, duration=duration)

    def circular_motion(self, image, duration, radius=40):
        w, h = image.size
        img_np = np.array(image)

        def make_frame(t):
            angle = 2 * np.pi * (t / duration)
            x = int(radius * np.cos(angle))
            y = int(radius * np.sin(angle))
            frame = Image.new("RGB", (w, h), (0, 0, 0))
            frame.paste(Image.fromarray(img_np), (x, y))
            return np.array(frame)

        return VideoClip(make_frame, duration=duration)
    
    def add_text_overlay(self, base_clip, text, color='white'):
        wrapped = textwrap.wrap(text.upper(), width=40)
        # Each slice of 2 lines forms a separate overlay
        lines = []
        while wrapped:
            lines.append('\n'.join(wrapped[:2]))
            wrapped = wrapped[2:]
        # For simplicity, return one combined overlay with the first chunk
        # (extend logic if you want multiple overlays for longer texts)
        font_path = os.path.join(self.fonts_folder, 'ARIALBD.TTF')
        if lines:
            txt_clip = TextClip(
                txt=lines[0],
                # size=48,
                font=font_path,
                color=color,
                method='caption',
                align='center',
                stroke_color='black',
                stroke_width=3,
                size=(int(base_clip.w * 0.8), int(base_clip.h * 0.2)),
                ).set_duration(base_clip.duration).set_position(('center', 0.8), relative=True)
            return CompositeVideoClip([base_clip, txt_clip]) #.set_duration(base_clip.duration)
        return base_clip
    
        #TODO: not great, but can be used as a starting point
        # https://github.com/aengus126/Caption-Generator-MoviePy/tree/main/release%201