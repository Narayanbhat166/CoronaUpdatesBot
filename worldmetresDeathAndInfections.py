import requests
import time
import datetime
import json
from bs4 import BeautifulSoup

FILE_NAME = 'World_Metres.json'


def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = '784469586'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)


def load():
    res = {}
    with open(FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


URL = 'https://www.worldometers.info/coronavirus/'


interested_countries = ['USA', 'India', 'Spain',
                        'Italy', 'Pakistan', 'Iran', 'Netherlands']

data = {}

while True:
    past_data = load()
    message = ''
    page = requests.get(url=URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    main_table = soup.find('div', class_='main_table_countries_div')

    rows = main_table.find_all('tr')
    for row in rows:
        for ele in rows:
            country = ele.getText().split('\n')[1]
            if country in interested_countries:
                temp = list(ele.getText().replace(
                    ',', '').replace('+', '').split('\n'))

                if past_data[country]['Infected'] != int(temp[2]):

                    message += "New " + \
                        str(int(temp[2]) - past_data[country]
                            ['Infected']) + " Infections in "+country+"\n"
                    past_data[country]['Infected'] = int(temp[2])

                if past_data[country]['Deaths'] != int(temp[4]):

                    message += "New " + \
                        str(int(temp[4]) - past_data[country]
                            ['Deaths'])+" Deaths in "+country+"\n"
                    past_data[country]['Deaths'] = int(temp[4])

        break
    if message != '':
        save(past_data)
        telegram_bot_sendtext(message)
        print(message)
    else:
        print("last checked at: " +
              str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))+" No changes")

    time.sleep(60)
