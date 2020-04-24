"""
Получаем данные о динамике распространения COVID-19 с карты Яндекса
"""


from bs4 import BeautifulSoup as bs
import requests
import json


class CovidData:
    def __init__(self):
        url = 'https://yandex.ru/maps/covid19'
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        jsons = soup.find("script", {"class": "config-view", "type": "application/json"}).string
        try:
            data = json.loads("".join(jsons))
            self.data = data['covidData']['items']
            """ Список словарей типа:
                {'name': 'Челябинская область', 'ru': True, 'cases': 61, 'cured': 29, 'deaths': 0,
                'coordinates': ['60.395641', '54.446199'], 'rid': 11225, 'histogram': [{'ts': 1584748800, 'value': 1},...]}
            """
        except:
            print("Ошибка в полученных данных")
            exit(1)

    def first_rus(self):  # Получить номер первого Российского региона
        for i, el in enumerate(self.data):
            if el['name'].upper() == "АЛТАЙСКИЙ КРАЙ":
                return i
        return 0

    def region_data(self, reg) -> dict:  # Получаем данные по названию региона
        for el in reversed(self.data):
            if el['name'].upper() == reg.upper():
                return el
        print("Ошибка! Неверно указан регион, либо он исчез с лица Земли.")
        exit(1)


if __name__ == '__main__':

    snapshot = CovidData()
    print(snapshot.data)
