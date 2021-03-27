# Instagram bot COVID19

![](Brazil-Flag.png) [README in Portuguese](LEIAME.md)

This bot searches for the number of deaths by COVD-19 in Brazil, generate an image with black background, and the number of deaths written in white. Then, upload the image to an [Instagram Profile](https://www.instagram.com/covid19_mortes/).

I really hope these numbers stop growing. I made this with the purpose to inform and sensitize the population about the chaotic state of the pandemic using a social media.


![Insta post example](25-03-2021.jpeg)
>Insta post day 25/03/2021


## Dependencies
We'll make [Web Scraping](https://bit.ly/3qOY5Pa) with [Requests](https://pypi.org/project/requests/) and [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to get the data we need.

Also, we'll use [Pillow](https://pillow.readthedocs.io/en/stable/) for generating the image and, [Insta bot](https://pypi.org/project/instabot/) to upload that image to Instagram.

Install all dependencies from [``requirements.txt``](requirements.txt).

````shell
pip install -r requirements.txt
````
## Run the bot
After install dependencies, fill ``username`` and ``password`` in the ``main.py`` file.

````Python3
bot.login(username="", password="", ask_for_code=True)
````

Run the [``main.py``](main.py)
````shell 
python main.py
````
Then, you can use [crontab](https://opensource.com/article/17/11/how-use-cron-linux) in Linux to schedule the script execution — or something similar for other OS.


## Code Explanation
### Importing the modules
````Python3
import requests
import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
````

### Starting the bot and Instagram Login
Instantiate ``Bot`` class from ``instabot`` module an use the ``login()`` function.
````Python3
bot = Bot()
bot.login(username="your_username", password="your_password", ask_for_code=True)
````

### Getting the deaths number
First we define our search ``url``. Then, we use requests ``get()`` method passing the ``url`` and store the following response in the variable ``r``.
````Python3
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
````

Now, with BeautifulSoup we pass the ``r.text`` and parse it to ``html`` storing it in the variable ``s``.
````Python3
s = BeautifulSoup(r.text, 'html.parser')
````
Analysing the [page](https://www.worldometers.info/coronavirus/country/brazil/) we can see the deaths number is a ``span`` element that is child from a ``div`` with class name ``maincounter-number``.

So, we'll use this class name to search for the specific element that contains the deaths number using ``find_all()`` and ``find()`` methods from BeautifulSoup and store it in the variable ``deaths``.
````Python3
deaths = s.find_all('div', {'class': "maincounter-number"})
deaths = deaths[1].find('span').text
````

### Creating image
With ``Pillow`` we can use ``Image.new()`` to create an image as our background defining ``RGB`` as the color format, ``width`` and ``height`` as ``1080px``, witch is the Instagram post format and, set the color to black using the ``RGB COLOR CODE``.
````Python3
img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
d = ImageDraw.Draw(img)
````

Define the font that you want and the size.
````Python3
# Windows Fonts Path
fnt = ImageFont.truetype(r"/Windows/Fonts/Arial.ttf", 200)
# Linux/MacOS Fonts Path
fnt = ImageFont.truetype(r"/Library/Fonts/Arial.ttf", 200)
````

Create the text and store the ``width`` and ``height`` of the text to centralize it in the background.
````Python3
w, h = d.textsize(deaths, font=fnt)
````

Calculate the center point by subtracting text size from the background size — in this case 1080px. Then, set the value of the text with ``deaths`` variable, set the ``font`` and Finally, set the text fill color to white using the ``RGB COLOR CODE``.
````Python3
d.text(((1080-w) / 2, (1080-h) / 2), deaths, font=fnt, fill=(255, 255, 255))
````

Now that we generated image, we can save it with current day name for identification.
````Python3
img_name = "{:%d-%m-%Y}.jpeg"
img_name = img_name.format(datetime.datetime.now())
img.save(img_name)
````

Finally, upload the image to Instagram.
````Python3
bot.upload_photo(img_name, caption="Insert Caption Here")
````
## Contribute
That's all. Feel free for collaborating with this repo. Thank you.