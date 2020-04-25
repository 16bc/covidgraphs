"""
Получаем данные о динамике распространения COVID-19 с карты Яндекса
"""


from bs4 import BeautifulSoup as bs
import requests
import json
import time


class CovidData:
    def __init__(self):
        url = 'https://yandex.ru/maps/covid19'
        cache_timeout = 300
        timenow = time.time()
        cache = self._read_cache()   # [timestamp, {some_data}] or [0]
        if timenow - cache[0] > cache_timeout:
            self.data = self._get_remote_data(url)
            self._write_cache(self.data)
        else:
            self.data = cache[1]
            print("Fetching data from cache")

    def _read_cache(self):
        try:
            with open("cache.json", 'r') as file:
                return json.load(file)
        except:
            return [0]

    def _write_cache(self, data):
        timestamp = time.time()
        with open("cache.json", 'w') as file:
            json.dump([timestamp, data], file, indent=2, ensure_ascii=False)

    def _get_remote_data(self, url):
        """
        Парсит сайт и возвращает список словарей типа:
            {'name': 'Челябинская область', 'ru': True, 'cases': 61, 'cured': 29, 'deaths': 0,
            'coordinates': ['60.395641', '54.446199'], 'rid': 11225, 'histogram': [{'ts': 1584748800, 'value': 1},...]}
        """
        print("Fetching remote data...")
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        jsons = soup.find("script", {"class": "config-view", "type": "application/json"}).string
        try:
            data = json.loads("".join(jsons))
            return data['covidData']['items']
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
