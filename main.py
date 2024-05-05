import re
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript('5Wi06-8xFu0', languages=['ja'])
# Regular expression pattern to match Japanese characters
japanese_pattern = re.compile(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+')

# Function to check if a character is ASCII
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Extract Japanese text from transcript and filter out English text
japanese_text = []
for item in transcript:
    if japanese_pattern.search(item['text']):
        japanese_text.append(''.join(filter(lambda x: not is_ascii(x), item['text'])))

# Join the Japanese text into a single string
japanese_text_str = '\n'.join(japanese_text)

from selenium import webdriver
from selenium.webdriver.common.by import By


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
# Close the WebDriver

