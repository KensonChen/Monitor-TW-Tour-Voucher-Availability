import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

options = webdriver.ChromeOptions()
options.add_argument('--headless=new') # Uses newer, more realistic headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Disguise the cloud browser as a real desktop user to bypass basic bot blockers
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)

url = "https://halfdaytour.taiwan.net.tw/Schedule/self"
webhook = os.environ.get("https://discord.com/api/webhooks/1527996637090156655/vomkN8m9D7pZ4qdDVMdiffubP6iBg2xiHzQNlJZcZ-Nm4GDGhMTZK3AaL4dFM9pJoC9e")

try:
    driver.get(url)
    
    # Put your copied selector inside the quotes below
    selector = "td[data-date='2026-07-19'] .fc-event-title"
    
    # Wait up to 15 seconds for the calendar element to load
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    
    quota = element.text.strip()
    
    if quota == "0":
        requests.post(webhook, json={"content": f"🚨 TAIWAN TOUR ALERT! Quota is {quota}. Book now: {url}"})
        print(f"Alert sent! Quota is {quota}")
    else:
        print("Quota is still 0. No alert sent.")
        
except Exception as e:
    print("\n--- DEBUGGING INFORMATION ---")
    print(f"Error Type: {type(e).__name__}")
    print(f"The server thinks the page title is: '{driver.title}'")
    print("If the title above mentions 'Cloudflare', 'Blocked', or 'Just a moment', the site is blocking the cloud server.")
    print("-----------------------------\n")
    traceback.print_exc()
finally:
    driver.quit()
