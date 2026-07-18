import os
import base64
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# --- PASTE YOUR ENCODED WEBHOOK STRING HERE ---
ENCODED_WEBHOOK = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTUyNzk5NjYzNzA5MDE1NjY1NS92b21rTjhtOUQ3cFo0cWREVk1kaWZmdWJQNmlCZzJ4aUh6UU5sSlpjWi1ObTRHREdoTVRaSzNBYUw0ZEZNOXBKb0M5ZQ=="
webhook = base64.b64decode(ENCODED_WEBHOOK).decode('utf-8')

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)
url = "https://halfdaytour.taiwan.net.tw/Schedule/self"

try:
    driver.get(url)
    
    # Exact CSS selector we found earlier
    selector = "td[data-date='2026-07-19'] .fc-event-title"
    
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    
    quota = element.text.strip()
    
    # Using == for the test!
    if quota != "0":
        requests.post(webhook, json={"content": f"🚨 TAIWAN TOUR ALERT! Quota is {quota}. Book now: {url}"})
        print(f"Alert sent! Quota is {quota}")
    else:
        print("Quota is still 0. No alert sent.")
        
except Exception as e:
    print("\n--- DEBUGGING INFORMATION ---")
    print(f"Error Type: {type(e).__name__}")
    print(f"The server thinks the page title is: '{driver.title}'")
    traceback.print_exc()
finally:
    driver.quit()
