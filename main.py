# Importing packages
from __future__ import unicode_literals
import re
import subprocess
import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import tkinter as tk
from tkinter import simpledialog

# Setting up ffmpeg for pydub
AudioSegment.ffmpeg = "C:/Program Files/ffmpeg-2024-05-02-git-71669f2ad5-essentials_build/bin/ffmpeg.exe"

# Function to check if a character is ASCII
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Function to download audio from YouTube and convert it to .wav
def download_from_url(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'C:/Users/Simon PC/Desktop/YouTubeInput/input.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        output_filename = filename.rsplit(".", 1)[0] + ".wav"
        subprocess.call(["C:/Program Files/Audacity/audacity.exe", output_filename])

# Function to handle submit button click
def submit_button_clicked(entry):
    url = entry.get()
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if not video_id:
        tk.messagebox.showerror("Error", "Invalid YouTube URL. Please provide a valid URL.")
        return

    # Get transcript from YouTube
    transcript = YouTubeTranscriptApi.get_transcript(video_id[0], languages=['ja'])

    # Regular expression pattern to match Japanese characters
    japanese_pattern = re.compile(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+')

    # Extract Japanese text from transcript and filter out English text
    japanese_text = [item['text'] for item in transcript if japanese_pattern.search(item['text'])]

    # Join the Japanese text into a single string
    japanese_text_str = '\n'.join(japanese_text)

    # Initialize the WebDriver
    driver = webdriver.Firefox()

    # Open the OJAD website
    driver.get("https://www.gavo.t.u-tokyo.ac.jp/ojad/eng/phrasing/index")

    # Find the textarea element by ID
    text_area = driver.find_element(By.ID, "PhrasingText")

    # Input the Japanese text string into the textarea
    text_area.send_keys(japanese_text_str)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_button.click()

    # Download and convert audio
    download_from_url(url)

# Create GUI window
root = tk.Tk()
root.title("YouTube Downloader")

# Create entry widget for URL input
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=lambda: submit_button_clicked(entry))
submit_button.pack(pady=5)

# Run the GUI window
root.mainloop()
