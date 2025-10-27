from pytubefix import YouTube
import moviepy.editor as mp
import os
import tkinter as tk
from tkinter import filedialog

def download_high_res(url, save_path):
    yt = YouTube(url)
    print(f"Title: {yt.title}")
    
    # Video-only 1080p
    video_stream = yt.streams.filter(adaptive=True, file_extension="mp4", res="1080p").first()
    if not video_stream:
        # fallback to 720p progressive
        video_stream = yt.streams.filter(progressive=True, file_extension="mp4", res="720p").first()
    if not video_stream:
        video_stream = yt.streams.get_highest_resolution()
    
    # Audio-only
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download streams
    video_file = os.path.join(save_path, "video.mp4")
    audio_file = os.path.join(save_path, "audio.mp4")
    final_file = os.path.join(save_path, f"{yt.title}.mp4")
    
    video_stream.download(output_path=save_path, filename="video.mp4")
    audio_stream.download(output_path=save_path, filename="audio.mp4")
    
    # Merge using moviepy
    video_clip = mp.VideoFileClip(video_file)
    audio_clip = mp.AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_file, codec="libx264", audio_codec="aac")
    
    # Cleanup temporary files
    os.remove(video_file)
    os.remove(audio_file)
    print("✅ 1080p Video downloaded and merged successfully!")
