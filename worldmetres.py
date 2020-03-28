import requests
import time
from bs4 import BeautifulSoup

FILE_NAME = 'Infected_count.dat'

URL = 'https://www.worldometers.info/coronavirus/country/india/'

while True:

    with open(FILE_NAME, 'r') as f:
        last = int(f.read())

    page = requests.get(url=URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    present = soup.find('div', class_='maincounter-number')
    if present:
        present = present.getText()
        present = int(present.replace(',', ''))

    if present != last:
        print(str(present - last) + " New Infections")
        with open(FILE_NAME, 'w') as f:
            f.write(str(present))

    time.sleep(30)
