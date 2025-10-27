from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog
import re

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"\rDownloading... {percentage:.2f}%", end="")

def normalize_youtube_url(url):
    match = re.search(r"(?:shorts/|watch\?v=)([\w-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("Invalid YouTube URL format!")

def download_video(url, save_path):
    try:
        url = normalize_youtube_url(url)
        yt = YouTube(url, on_progress_callback=progress_function)
        print(f"\nTitle: {yt.title}")
        print(f"Author: {yt.author}")

        # Try to get 1080p first, if not available fallback to 720p
        stream = yt.streams.filter(progressive=True, file_extension="mp4", res="1080p").first()
        if not stream:
            stream = yt.streams.filter(progressive=True, file_extension="mp4", res="720p").first()
        if not stream:
            # fallback to highest resolution available
            stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()

        print(f"Resolution: {stream.resolution}")
        print("Downloading started...\n")
        stream.download(output_path=save_path)
        print("\n✅ Video downloaded successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    video_url = input("Please enter a YouTube URL: ")
    save_dir = open_file_dialog()

    if save_dir:
        print("Preparing to download...")
        download_video(video_url, save_dir)
    else:
        print("Invalid save location.")
