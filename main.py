import requests
import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot

# Start bot and login
bot = Bot()
bot.login(username="username", password="password", ask_for_code=True)

# Scrape Worldometers website
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
s = BeautifulSoup(r.text, 'html.parser')
deaths = s.find_all('div', {'class': 'maincounter-number'})
deaths = deaths[1].find('span').text
print(deaths)

# Create Image
img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
d = ImageDraw.Draw(img)
fnt = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 200)
w, h = d.textsize(deaths, font=fnt)
d.text(((1080-w)/2, (1080-h)/2), deaths, font=fnt, fill=(255, 255, 255))

# Save Image with datetime name
img.save(f'{datetime.datetime.now():%d-%m-%Y}.jpeg')

# Store the name of the image
img_name = f'{datetime.datetime.now():%d-%m-%Y}.jpeg'
print(img_name)

# Upload Image
bot.upload_photo(img_name, caption=f'Dia {datetime.datetime.now():%d/%m/%Y} chegamos ao triste número de {deaths} brasileiros mortos por conta da COVID-19. Fonte:https://www.worldometers.info/coronavirus/country/brazil/')
