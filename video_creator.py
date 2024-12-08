import os

from gtts import gTTS
from moviepy import ImageClip, CompositeVideoClip, AudioFileClip

def create_video_summary(summary, language="en"):
    clips = []

    tts = gTTS(summary, lang=language)
    tts.save(f"temp_audio_in_{language}.mp3")
    
    
    clip = ImageClip("placeholder.jpg", duration=18)
    clip = clip.with_duration(5).with_position("center")
    clips.append(clip)
   
    video = CompositeVideoClip(clips)
    audio = AudioFileClip(f"temp_audio_in_{language}.mp3")
    video = video.with_audio(audio)
    video.write_videofile(f"beauty_summary_in_{language}.mp4", fps=24)

    if os.path.exists(f"temp_audio_in_{language}.mp3"):
        os.remove(f"temp_audio_in_{language}.mp3")

