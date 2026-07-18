{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import time\
import threading\
import requests\
from flask import Flask\
from selenium import webdriver\
from selenium.webdriver.chrome.service import Service\
\
app = Flask(__name__)\
\
# This route is our "keep-alive" endpoint for Render\
@app.route('/')\
def home():\
    return "Monitor is running!"\
\
def run_monitor():\
    # Cloud-safe Chrome configuration\
    options = webdriver.ChromeOptions()\
    options.add_argument('--headless')\
    options.add_argument('--no-sandbox')\
    options.add_argument('--disable-dev-shm-usage')\
    \
    # Point Selenium to the Docker-installed driver\
    service = Service('/usr/bin/chromedriver')\
    driver = webdriver.Chrome(service=service, options=options)\
    \
    url = "https://halfdaytour.taiwan.net.tw/Schedule/self"\
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")\
\
    while True:\
        try:\
            driver.get(url)\
            time.sleep(5) \
            \
            # TODO: Add your specific element locator here\
            quota = "0" \
            \
            if quota != "0":\
                requests.post(webhook, json=\{"content": f"\uc0\u55357 \u57000  TAIWAN TOUR ALERT! Quota: \{quota\}. Book: \{url\}"\})\
                break \
        except Exception as e:\
            print(f"Scraping error: \{e\}")\
            \
        time.sleep(120)\
\
if __name__ == '__main__':\
    # Start the Selenium loop in the background\
    threading.Thread(target=run_monitor, daemon=True).start()\
    # Start the dummy web server so Render registers the app as 'live'\
    port = int(os.environ.get("PORT", 10000))\
    app.run(host='0.0.0.0', port=port)}