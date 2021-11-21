import sqlite3
from random import randint
import requests
from bs4 import BeautifulSoup

__all__ = ['olx']


URL_1 = 'https://www.olx.ua/transport/'
URL_2 = 'https://auto.ria.com/newauto/search/'
HEADERS = [
    {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/96.0.4664.55 Mobile Safari/537.36',
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
               'application/signed-exchange;v=b3;q=0.9'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
               'application/signed-exchange;v=b3;q=0.9'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
        'application/signed-exchange;v=b3;q=0.9'}
    ]


def olx(url=URL_1, params=None):
    data = []
    errors = []
    if url:
        r = requests.get(url, headers=HEADERS[randint(0, 2)], params=params)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            item_desk = soup.find('table', class_='fixed offers breakword redesigned')
            if item_desk:
                item_cards = item_desk.find_all('div', class_='offer-wrapper')
                for item in item_cards:
                    try:
                        item_photo = item.find('img').get('src')
                    except:
                        item_photo = 'Нет фото'
                    item_city = item.find('td', class_='bottom-cell').find('small', class_='breadcrumb x-normal'). \
                        find('span').text
                    item_title = item.find('h3', class_='lheight22 margintop5').text.strip()
                    item_price = item.find('p', class_='price').text.strip()
                    item_url = item.find('h3', class_='lheight22 margintop5').find('a').get('href')

                    data.append({
                        'item_photo': item_photo,
                        'item_city': item_city,
                        'item_title': item_title,
                        'item_price': item_price,
                        'item_url': item_url
                    })

                    data.append((item_photo, item_city, item_title, item_price, item_url))

            else:
                errors.append({'url': url, 'title': "Div does not exists"})

        else:
            errors.append({'url': url, 'title': "Page do not response"})

    # conn = sqlite3.connect('data/olx.db')
    #
    # sql_insert_query = '''INSERT INTO item_olx (item_photo, item_city, item_title, item_price, item_url)
    #                         VALUES (?, ?, ?, ?, ?)'''
    #
    # cursor = conn.cursor()
    # cursor.executemany(sql_insert_query, data[0])
    #
    # conn.commit()
    # conn.close()

    return data[0], errors


def auto_ria(url=URL_2):
    data = []
    errors = []
    if url:
        r = requests.get(url, headers=HEADERS[randint(0, 2)], params=None)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            item_desk = soup.find('div', id='searchResults')
            another_item_desk = soup.find('div', class_='result-explore')
            if item_desk:
                item_cards = item_desk.find_all('section', class_='ticket-item')
                for item in item_cards:
                    item_photo = item.find('picture').find('img').get('src')
                    item_city = item.find('li', class_='view-location').text.replace('( от )', '').strip()
                    item_title = item.find('div', class_='item ticket-title').find('a').text.strip()
                    item_price = item.find('div', class_='price-ticket').find('span', class_='bold green size22').text
                    item_url = item.find('div', class_='ticket-photo').find('a').get('href')

                    data.append({
                        'item_photo': item_photo,
                        'item_city': item_city,
                        'item_title': item_title,
                        'item_price': f'{item_price} $',
                        'item_url': item_url
                    })
            elif another_item_desk:
                another_item_cards = another_item_desk.find_all('section', class_='proposition')
                for another_item in another_item_cards:
                    another_item_photo = another_item.find('picture').find('img').get('src')
                    another_item_city = another_item.find('span', class_='item region').text.strip()
                    another_item_title = another_item.find('h3', class_='proposition_name').find('span').text.strip()
                    another_item_price = another_item.find('div', class_='proposition_price').find('span').text.strip()
                    another_item_url = another_item.find('a').get('href')

                    data.append({
                        'item_photo': another_item_photo,
                        'item_city': another_item_city,
                        'item_title': another_item_title,
                        'item_price': {another_item_price},
                        'item_url': f'https://auto.ria.com{another_item_url}'
                    })
            else:
                errors.append({'url': url, 'title': "Div does not exists"})

        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return data[0], errors


def main():
    # result_olx = olx(url=URL_1)
    # print(result_olx)
    result_autoria = (auto_ria())
    print(result_autoria)


if __name__ == '__main__':
    main()
