import os
from modules.base_generator import BaseGenerator
from moviepy.editor import AudioFileClip
from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, vfx


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

        for scene in video_dict['scenes']:
            for path in media_paths_dict:
                if scene['scene'] == path['scene']:
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
                video_clip = self.create_video_clip(media_path, audio_duration)

                # Add the audio to the video clip
                if audio_duration > 0:
                    audio_clip = AudioFileClip(voiceover_path)
                    video_clip = video_clip.set_audio(audio_clip)
                
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
        return final_video_path

        
            
            


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
        
        # Apply slide-in animation
        # Apply fade-in and fade-out animation
        for i in range(len(video_clips) - 1):
            video_clips[i] = video_clips[i].fx(vfx.fadeout, duration=0.2)
            video_clips[i + 1] = video_clips[i + 1].fx(vfx.fadein, duration=0.2)
            print("Fade-in and fade-out animation applied")
        
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(final_video_path, codec="libx264", fps=24)
        final_video.close()
        return final_video_path