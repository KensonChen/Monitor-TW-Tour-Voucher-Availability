import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# GitHub-friendly Chrome setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# GitHub automatically has Chrome installed for us
driver = webdriver.Chrome(options=options)

url = "https://halfdaytour.taiwan.net.tw/Schedule/self"
webhook = os.environ.get("DISCORD_WEBHOOK_URL")

try:
    driver.get(url)
    
    # TODO: Replace with the CSS selector you copied from the website
    selector = "PASTE_YOUR_COPIED_SELECTOR_HERE"
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    
    quota = element.text.strip()
    
    if quota != "0":
        requests.post(webhook, json={"content": f"🚨 TAIWAN TOUR ALERT! Quota is {quota}. Book now: {url}"})
        print(f"Alert sent! Quota is {quota}")
    else:
        print("Quota is still 0. No alert sent.")
        
except Exception as e:
    print(f"Error checking page: {e}")
finally:
    driver.quit() # Always close the browser to free up memory
