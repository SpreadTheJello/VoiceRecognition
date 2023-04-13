import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def click(element):
    time.sleep(0.1)
    element.click()

def get_random_video_url(browser):
    def _get_random_video_url():
        url = "https://www.youtube.com"

        # Get the current page source
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        video_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("/watch?v=")]


        if not video_links:
            return None
        
        video_links = video_links[:8]
        
        random_video_url = url + random.choice(video_links)
        print(random_video_url)
        return random_video_url
    return _get_random_video_url

def open_youtube(browser):
    def _open_youtube():
        browser.get("https://www.youtube.com/")
        print("--opened youtube--")
    return _open_youtube

def play_pause(browser):
    def _play_pause():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('k')
        print("--paused/played video--")
    return _play_pause

def homepage_random_video(browser):
    def _homepage_random_video():
        random_video_url = get_random_video_url(browser)()
        if random_video_url:
            browser.get(random_video_url)
            print("--played random video--")
        else:
            print("Failed to find a random video")
    return _homepage_random_video

def next_video(browser):
    def _next_video():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SHIFT + 'n')
        print("--played next video--")
    return _next_video

def mute_video(browser):
    def _mute_video():
        body = browser.find_element(By.TAG_NAME, 'body')
        body.send_keys('m')
        print("--muted/unmuted video--")
    return _mute_video

def homepage(browser):
    def _homepage():
        open_youtube_func = open_youtube(browser)
        open_youtube_func()
        print("--went to homepage--")
    return _homepage

def back_button(browser):
    def _back_button():
        browser.execute_script("window.history.go(-1)")
        print("--back button pressed--")
    return _back_button

def forward_button(browser):
    def _forward_button():
        browser.execute_script("window.history.go(1)")
        print("--forward button pressed--")
    return _forward_button

def main():
    driver_path = "/path/to/chromedriver"
    browser = webdriver.Chrome(driver_path)

    open_youtube(browser)

    browser.quit()

if __name__ == "__main__":
    main()
