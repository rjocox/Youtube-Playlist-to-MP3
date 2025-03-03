import os
import re
import yt_dlp
import time
from tkinter import messagebox

def sanitize_filename(name):
        return re.sub(r'[\/:*?"<>|]', '_', name)  # Replace invalid characters with "_"

def fetch_playlist(url):
    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube playlist URL.")
        return []

    try:
        ydl_opts = {'extract_flat': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                return [
                    (entry.get('title', 'Unknown Title'), entry.get('url'))
                    for entry in info['entries'] if entry.get('url')
                ]
            else:
                messagebox.showerror("Error", "No playlist found. Please check the URL.")
                return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch playlist: {e}")
        return []

def refresh_folder(path):
    try:
        os.system(f'explorer "{os.path.abspath(path)}"')
    except Exception as e:
        print(f"Failed to refresh folder: {e}")

def download_videos(selected_videos, save_path):
    if not selected_videos:
        messagebox.showerror("Error", "No items selected. Please select at least one item.")
        return

    if not save_path:
        messagebox.showerror("Error", "Please provide a valid save location.")
        return

    try:
        for title, video_url in selected_videos:
            sanitized_title = sanitize_filename(title)

            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'merge_output_format': 'mp3',
                'outtmpl': os.path.join(save_path, f'{sanitized_title}.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)


                filename = ydl.prepare_filename(info)
                base, ext = os.path.splitext(filename)


                if '-' in sanitized_title:
                    final_filename = os.path.join(save_path, sanitized_title + ext)
                    os.rename(filename, final_filename)
                    print(f"Renamed: {filename} → {final_filename}")


        time.sleep(1)


        refresh_folder(save_path)

        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")
