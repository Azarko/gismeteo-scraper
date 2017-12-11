# -*- coding: utf-8 -*-

__author__ = 'Boris Polyanskiy'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

html = urlopen('https://www.gismeteo.ru/weather-zelenograd-11443/10-days/')


class GisMeteoInfoScraper:
    def __init__(self, page):
        self.t_max_values = []
        self.t_min_values = []
        self.p_max_values = []
        self.p_min_values = []
        self.weather_labels = []
        self.wind_direction = []
        self.wind_force = []
        self.wind_max_force = []
        self.weather_day = []
        self.page_url = page
        self.html = None

    def start(self):
        html = self._get_page_content(self.page_url)
        if not html:
            return
        else:
            self.html = html
        bs = BeautifulSoup(self.html, 'html.parser')
        self.t_max_values, self.p_max_values = self.get_attr_by_parent(
            bs.find_all(class_='maxt'), 'data-widget-id', 'forecast', 'pressure')
        self.t_min_values, self.p_min_values = self.get_attr_by_parent(
            bs.find_all(class_='mint'), 'data-widget-id', 'forecast', 'pressure')
        self.weather_labels = [unit.attrs['data-text'] for unit in bs.find_all('span', class_='tooltip')]
        self.wind_direction = [unit.string.strip() for unit in bs.find_all(class_='w_wind__direction')]
        self.wind_force = [unit.string for unit in bs.find_all(class_='js_value val_to_convert')]
        self.wind_max_force = [unit.attrs['data-value'] for unit in bs.find_all(class_='w_wind__value widget__value')]
        self.weather_day = [unit.string.strip() for unit in bs.find_all(class_='w_date__date')][:10]
        weather = pd.DataFrame(
            {
                "period": self.weather_day,
                "short desc": self.weather_labels,
                "temp max": self.t_max_values,
                "temp min": self.t_min_values,
                "press max": self.p_max_values,
                "press min": self.p_min_values,
                "wind direction": self.wind_direction,
                "wind force": self.wind_force,
                "wind max force": self.wind_max_force
            }
        )
        print(weather)
        with open('out.html', 'w', encoding='utf-8') as f:
            f.write(weather.to_html(index=False))

    @staticmethod
    def get_attr_by_parent(units, parent_name, *attr):
        res = [[] for _ in range(len(attr))]
        for unit in units:
            for parent in unit.parents:
                if parent and parent_name in parent.attrs:
                    if parent.attrs[parent_name] in attr:
                        res[attr.index(parent.attrs[parent_name])].append(unit.string.replace('−', '-'))
        return res

    @staticmethod
    def _get_page_content(page):
        html = urlopen(page)
        if html.getcode() == 200:
            return html
        else:
            return False


class GisMeteoScraperApi:
    pass


if __name__ == '__main__':
    c = GisMeteoInfoScraper('https://www.gismeteo.ru/weather-zelenograd-11443/10-days/')
    c.start()
