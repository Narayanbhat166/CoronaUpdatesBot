import requests
import time
import datetime
from bs4 import BeautifulSoup

FILE_NAME = 'Infected_count.dat'


def telegram_bot_sendtext(bot_message):

    bot_token = '1132521081:AAHht4z1Eo00E86wcIZtGqYH1CshBxnQyk8'
    bot_chatID = '784469586'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


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

        test = telegram_bot_sendtext(
            "New Infections in India: "+str(present - last))
        if test['ok'] == True:
            print("Sent a Telegram message")
    else:
        print("last checked at: " +
              str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')))

    time.sleep(30)
