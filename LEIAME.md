# Instagram bot COVID19

Este bot consulta o número de mortes por COVD-19 no Brasil e então gera uma imagem com fundo preto e o número de mortos escrito em branco. Depois, envia a imagem através de um [Perfil do Instagram](https://www.instagram.com/covid19_mortes/).

Eu realmente espero que esses números parem de crescer. Fiz isso com o objetivo de informar e sensibilizar a população sobre o estado caótico da pandemia através de uma rede social.


![Insta post example](25-03-2021.jpeg)
> Post do dia 25/03/2021


## Dependências
Faremos [Web Scraping](https://bit.ly/3qOY5Pa) utilizando as bibliotecas [Requests](https://pypi.org/project/requests/) e [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) para extrair os dados de que precisamos.

Além disso, usaremos [Pillow](https://pillow.readthedocs.io/en/stable/) para gerar a imagem e [Insta bot](https://pypi.org/project/instabot/) para carregar a imagem no Instagram.

Instale todas as dependências a partir do arquivo [``requirements.txt``](requirements.txt).

````shell
pip install -r requirements.txt
````
## Execute o bot
Após instalar as dependências, preencha ``usuario`` e ``senha`` no arquivo ``main.py``.

````Python3
bot.login(username="", password="", ask_for_code=True)
````

Execute o [``main.py``](main.py)
````shell
python main.py
````
Você pode utilizar [crontab](https://opensource.com/article/17/11/how-use-cron-linux) no Linux para agendar a execução do script — ou alguma alternativa similar para outros Sistemas Operacionais.


## Explicação do código
### Importando os módulos
````Python3
import requests
import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
````

### Iniciando o bot e fazendo login no Instagram
Instancie a classe ``Bot`` do módulo ``instabot`` e use a função ``login()``.
````Python3
bot = Bot()
bot.login(username="seu_usuario", password="sua_senha", ask_for_code=True)
````

### Obtendo o número de mortes
Primeiro, definimos o `` url`` de consulta. Então, usamos o método ``get()`` da biblioteca requests, passando o `` url`` e armazenamos a resposta obtida na variável `` r``.
````Python3
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
````

Agora, com BeautifulSoup passamos o ``r.text`` e o estruturamos o código em ``html``, armazenando-o na variável `` s``.
````Python3
s = BeautifulSoup(r.text, 'html.parser')
````
Analisando a [página](https://www.worldometers.info/coronavirus/country/brazil/), identificamos que o número de mortes está num elemento ``span`` que é filho de uma ``div`` com classe de nome ``maincounter-number``.

Então, usaremos este nome de classe para pesquisar o elemento específico que contém o número de mortes usando os métodos ``find_all()`` e ``find()`` do BeautifulSoup e armazená-lo na variável ``deaths``.
````Python3
deaths = s.find_all('div', {'class': "maincounter-number"})
deaths = deaths[1].find('span').text
````

### Criando a imagem
Com ``Pillow`` podemos usar ``Image.new()`` para criar uma imagem, definindo ``RGB`` como o formato de cor, ``largura`` e ``altura`` como ``1080px``, que é o formato de postagem do Instagram e, definindo a cor para preto utilizando o ``CÓDIGO DE COR RGB``.
````Python3
img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
d = ImageDraw.Draw(img)
````

Defina a fonte desejada e o tamanho.
````Python3
# Caminho das fontes do Windows
fnt = ImageFont.truetype(r"/Windows/Fonts/Arial.ttf", 200)
# Caminho das fontes Linux / MacOS
fnt = ImageFont.truetype(r"/Library/Fonts/Arial.ttf", 200)
````

Crie o texto e armazene a ``largura`` e a ``altura`` do texto para centralizá-lo na imagem.
````Python3
w, h = d.textsize(deaths, font=fnt)
````

Calcule o ponto central subtraindo o tamanho do texto do tamanho da imagem — neste caso 1080px. Então, defina o valor do texto com a variável ``deaths``, defina a ``fonte`` e finalmente, defina a cor de preenchimento do texto para branco utilizando o ``CÓDIGO DE COR RGB``.
````Python3
d.text(((1080-w) / 2, (1080-h) / 2), deaths, font=fnt, fill=(255, 255, 255))
````

Agora que geramos a imagem, podemos salvá-la com o nome do dia atual para identificação.
````Python3
img_name = "{:%d-%m-%Y}.jpeg"
img_name = img_name.format(datetime.datetime.now())
img.save(img_name)
````

Por fim, envie a imagem para o Instagram.
````Python3
bot.upload_photo(img_name, caption="Inserir legenda aqui")
````
## Contribua
Isso é tudo. Sinta-se à vontade para colaborar com este repositório. Obrigado.