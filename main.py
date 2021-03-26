import requests
import datetime
import re
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
from sys import platform


# Start bot and login
bot = Bot()
bot.login(username="username", password="password", ask_for_code=True, use_cookie=False)

# Scrape Worldometers website
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
s = BeautifulSoup(r.text, 'html.parser')
deaths = s.find_all('div', {'class': "maincounter-number"})
deaths = deaths[1].find('span').text
updates = s.find('li', class_="news_li").find_all('strong')
new_cases = (re.search(r"\d+,\d+", updates[0].text).group())
new_deaths = (re.search(r"\d+,\d+", updates[1].text).group())

# Create background image
img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
d = ImageDraw.Draw(img)

# Check OS locate and set font
if platform == 'win32':
    fnt = ImageFont.truetype(r"/Windows/Fonts/Arial.ttf", 200)
else:
    fnt = ImageFont.truetype(r"/Library/Fonts/Arial.ttf", 200)

# Centralize text
w, h = d.textsize(deaths, font=fnt)
d.text(((1080 - w) / 2, (1080 - h) / 2), deaths, font=fnt, fill=(255, 255, 255))

# Save image with current date name
img_name = "{:%d-%m-%Y}.jpeg"
img_name = img_name.format(datetime.datetime.now())
img.save(img_name)

# Upload Image
caption = '''
{:%d/%m/%Y} - Chegamos ao triste número de {} brasileiros mortos por conta da COVID-19.

São {} mortos e {} novos casos somente nas últimas 24 horas.

Fonte:https://www.worldometers.info/coronavirus/country/brazil/
'''
bot.upload_photo(img_name, caption=caption.format(datetime.datetime.now(), deaths, new_deaths, new_cases))
