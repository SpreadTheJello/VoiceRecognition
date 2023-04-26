import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Function to click an element after a small delay
def click(element):
    time.sleep(0.1)
    element.click()

# Function to get a random video URL from the current page
def get_random_video_url(browser):
    def _get_random_video_url():
        url = "https://www.youtube.com"

        # Get the current page source
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all video links on the page
        video_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("/watch?v=")]

        # If no video links found, return None
        if not video_links:
            return None
        
        # Get the first 8 video links (prevents unseen videos being clicked) and choose a random one
        video_links = video_links[:8]
        random_video_url = url + random.choice(video_links)
        print(random_video_url)
        return random_video_url
    return _get_random_video_url

# Function to open YouTube homepage
def open_youtube(browser):
    def _open_youtube():
        browser.get("https://www.youtube.com/")
        print("--opened youtube--")
    return _open_youtube

# Function to play or pause the current video
def play_pause(browser):
    def _play_pause():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('k')
        print("--paused/played video--")
    return _play_pause

# Function to play a random video from the homepage
def homepage_random_video(browser):
    def _homepage_random_video():
        random_video_url = get_random_video_url(browser)()
        if random_video_url:
            browser.get(random_video_url)
            print("--played random video--")
        else:
            print("Failed to find a random video")
    return _homepage_random_video

# Function to play the next video in the queue
def next_video(browser):
    def _next_video():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SHIFT + 'n')
        print("--played next video--")
    return _next_video

# Function to stop listening
def stop_listening():
    def _stop_listening():
        print("--stopped listening--")
    return _stop_listening

# Function to mute or unmute the current video
def mute_video(browser):
    def _mute_video():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('m')
        print("--muted/unmuted video--")
    return _mute_video

# Function to enter fullscreen mode
def fullscreen(browser):
    def _fullscreen():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('f')
        print("--fullscreen button--")
    return _fullscreen

# Function to enter theatre mode
def theater_mode(browser):
    def _theater_mode():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('t')
        print("--theatre mode button--")
    return _theater_mode

# Function to navigate to the YouTube homepage
def homepage(browser):
    def _homepage():
        open_youtube_func = open_youtube(browser)
        open_youtube_func()
        print("--went to homepage--")
    return _homepage

# function pick video from home page and play it example : "play video 1" or "play video 2" etc
# def play_video(browser, video_number):
#     def _play_video():
#         open_youtube_func = open_youtube(browser)
#         open_youtube_func()
#         time.sleep(1)
#         body = browser.find_element(By.TAG_NAME, 'body')
#         body.send_keys(Keys.SHIFT + video_number)
#         print("--played video--")
#     return _play_video

# Function to navigate back in the browser history
def back_button(browser):
    def _back_button():
        browser.execute_script("window.history.go(-1)")
        print("--back button pressed--")
    return _back_button

# Function to navigate forward in the browser history
def forward_button(browser):
    def _forward_button():
        browser.execute_script("window.history.go(1)")
        print("--forward button pressed--")
    return _forward_button

# Main function to run the script
def main():
    driver_path = "/path/to/chromedriver"
    browser = webdriver.Chrome(driver_path)

    open_youtube(browser)

    browser.quit()

if __name__ == "__main__":
    main()
