import requests
import re
from bs4 import BeautifulSoup



class Weather:
    def __init__(self, city):
        self.__city = city
        self.__url = f'https://yandex.ru/pogoda/{city}'

        # Чтобы в каждый метод не вставлять запрос и не плодить запросы.
        self.__response = self.get_html()

    def get_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/'
                          '537.36 (HTML, like Gecko) Chrome/'
                          '128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'
        }
        response = requests.get(self.__url, headers=headers)
        return response


    def get_current(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        temp_now = f'{soup.find('div', attrs={
            'class': 'temp fact__temp fact__temp_size_s'}).get_text()}°C'
        return temp_now


    def get_annotation(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        annotation = soup.find('div', attrs={
            'class': 'link__condition day-anchor i-bem'}).get_text()
        return annotation

    def get_feeling(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        feeling = f'{soup.find('div', attrs={
            'class': 'term term_orient_h fact__feels-like'}).find
            ('div', attrs={'class': 'term__label'}).get_text()} {soup.find('div', attrs={
            'class': 'term term_orient_h fact__feels-like'}).find
            ('span', attrs={'class': 'temp__value temp__value_with-unit'}).text}°C'
        return feeling

    def get_wind(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        wind = (f'{soup.find('div', attrs={
            'class': 'term term_orient_v fact__wind-speed'}).find(
            'span', attrs={'class': 'wind-speed'}).get_text()} '
                f'{soup.find('div', attrs={
            'class': 'term term_orient_v fact__wind-speed'}).find(
            'span', attrs={'class': 'fact__unit'}).get_text()}')
        return wind

    def get_humidity(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        humidity = soup.find(
            'div',
            attrs={'class': 'term term_orient_v fact__humidity'}).find(
            'div', attrs={'class': 'term__value'}).text
        return humidity

    def get_pressure(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        pressure = soup.find(
            'div', attrs={'class':
                              'term term_orient_v fact__pressure'}).find(
            'div', attrs={'class': 'term__value'}).text
        return pressure

    def get_forecast(self):
        soup = BeautifulSoup(self.__response.text, "html.parser")
        list_forecast = []
        forecast = soup.find(
            'a', attrs={
                'href': re.compile('tomorrow')}).text
        list_forecast.append(forecast)

        forecast = soup.find(
            'a', attrs={
                'class':
                    'link link_theme_normal text forecast-briefly__day-link i-bem',
                'href': re.compile('day-2')}).text
        list_forecast.append(forecast)

        forecast = soup.find(
            'a', attrs={
                'href': re.compile('day-3')}).text
        list_forecast.append(forecast)


        return list_forecast


if __name__ == '__main__':

    weather = Weather('moscow')

    print(weather.get_current())
    print(weather.get_annotation())
    print(weather.get_feeling())
    print(weather.get_wind())
    print(weather.get_humidity())
    print(weather.get_pressure())
    print(weather.get_forecast())

    # moscow
    # nizhny-novgorod
    # sochi
    # novosibirsk
    # london
    # delhi


