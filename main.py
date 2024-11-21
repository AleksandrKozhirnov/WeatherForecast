import requests
import re
from bs4 import BeautifulSoup


class Weather:
    """
    Класс запрашивает погоду с сайта Яндекс Погода для указанного города.
    """

    def __init__(self, city: str):
        """
        Устанавливает атрибуты для объекта класса.
        Args:
            city: Город, для которого запрашивается погода.
            Вводится латинскими буквами.

            url: Адрес с которого запрашивается погода. Представляет
            собой конструктор.

            response: Ответ, получаемый с сайта в виде html.
        """
        self.__city = city
        self.__url = f'https://yandex.ru/pogoda/{city}'
        self.__response = self.get_html()

    def get_html(self):
        """
        Returns:
            Возвращает ответ с сайта Яндекс погода в виде html.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/'
                          '537.36 (HTML, like Gecko) Chrome/'
                          '128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'
        }
        response = requests.get(self.__url, headers=headers)
        return response

    def get_current(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            о текущей температуре в полученном ответе html.

        Returns:
            Возвращает текущую температуру в °C.

        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        temp_now = f'{soup.find('div', attrs={
            'class': 'temp fact__temp fact__temp_size_s'}).get_text()}°C'
        return temp_now

    def get_annotation(self):
        """
            Использует библиотеку BeautifulSoup, для поиска
            описания погоды в полученном ответе html.

        Returns:
            Возвращает описание текущей погоды (облачно, ясно, идет
            дождь и т.д.)
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        annotation = soup.find('div', attrs={
            'class': 'link__condition day-anchor i-bem'}).get_text()
        return annotation

    def get_feeling(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            об ощущаемой температуре в полученном ответе html.

        Returns:
            Возвращает информацию об ощущаемой температуре (например:
            'ощущается как −3°C')
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        feeling = (f'{soup.find('div', attrs={
            'class': 'term term_orient_h fact__feels-like'}).find
            ('div', attrs={'class': 'term__label'}).get_text()} '
                   f'{
                   soup.find('div', attrs={
                       'class': 'term term_orient_h fact__feels-like'}).find
            ('span', attrs={'class': 'temp__value temp__value_with-unit'}
             ).text}°C')
        return feeling

    def get_wind(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            о скорости и направлении ветра в полученном ответе html.

        Returns:
            Возвращает информацию о скорости и направлении ветра.
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        wind = (f'{soup.find('div', attrs={
            'class': 'term term_orient_v fact__wind-speed'}).find(
            'span', attrs={'class': 'wind-speed'}).get_text()} '
                f'{soup.find('div', attrs={
                  'class': 'term term_orient_v fact__wind-speed'}).find(
                  'span', attrs={'class': 'fact__unit'}).get_text()}')
        return wind

    def get_humidity(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            о текущей влажности в полученном ответе html.

        Returns:
            Возвращает информацию о влажности воздуха.
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        humidity = soup.find(
            'div',
            attrs={'class': 'term term_orient_v fact__humidity'}).find(
            'div', attrs={'class': 'term__value'}).text
        return humidity

    def get_pressure(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            об атмосферном давлении в полученном ответе html.

        Returns:
            Возвращает информацию об атмосферном давлении.
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        pressure = soup.find(
            'div', attrs={
                'class': 'term term_orient_v fact__pressure'}).find(
                  'div', attrs={'class': 'term__value'}).text
        return pressure

    def get_forecast(self):
        """
            Использует библиотеку BeautifulSoup, для поиска информации
            о прогнозе погоды на 3 дня в полученном ответе html.

        Returns:
            Возвращает информацию о прогнозе погоды на 3 дня
            в виде списка.
        """
        soup = BeautifulSoup(self.__response.text, "html.parser")
        list_forecast = []
        forecast = soup.find(
            'a', attrs={'href': re.compile('tomorrow')}
                            ).get_text(' ')
        list_forecast.append(forecast)

        forecast = soup.find(
            'a', attrs={
                'class':
                'link link_theme_normal text forecast-briefly__day-link i-bem',
                'href': re.compile('day-2')}).get_text(' ')
        list_forecast.append(forecast)

        forecast = soup.find(
            'a', attrs={
                'href': re.compile('day-3')}).get_text(' ')
        list_forecast.append(forecast)

        return list_forecast


if __name__ == '__main__':

    weather = Weather('novosibirsk')

    print(weather.get_current())
    print(weather.get_annotation())
    print(weather.get_feeling())
    print(weather.get_wind())
    print(weather.get_humidity())
    print(weather.get_pressure())
    print(weather.get_forecast())

    # Проверил несколько городов. Работает.
    # moscow
    # nizhny-novgorod
    # sochi
    # novosibirsk
    # london
    # delhi
