import os

from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    concatenate_audioclips,
    vfx,
    ffmpeg_tools
)

def merge_video_audio(image_vedio_file, audio_file, final_file):
    ffmpeg_tools.ffmpeg_merge_video_audio(image_vedio_file, audio_file, final_file)

def image_to_video(image_file, image_vedio_file, duration):
    clip = ImageClip(image_file).with_duration(duration)
    video_clip = concatenate_videoclips([clip], method='compose')
    video_clip.write_videofile(image_vedio_file, codec="libx264", fps=30, bitrate="5000k")

def merge_mp3_files(mp3_files, audio_file):
    audio_files = [AudioFileClip(f) for f in mp3_files]
    
    audio_clip = concatenate_audioclips(audio_files)
    audio_clip.write_audiofile(audio_file)

def get_audio_duration(audio_file):
    audio_clip = AudioFileClip(audio_file)
    return audio_clip.duration