# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

html = urlopen('https://www.gismeteo.ru/weather-zelenograd-11443/10-days/')


b = BeautifulSoup(html, 'html.parser')
forecast_max_values = []
forecast_min_values = []
pressure_max_values = []
pressure_min_values = []
for unit in b.find_all(class_='maxt'):
    for parent in unit.parents:
        if parent and 'data-widget-id' in parent.attrs:
            if parent.attrs['data-widget-id'] == 'forecast':
                forecast_max_values.append(unit.string.replace('−', '-'))
                break
            if parent.attrs['data-widget-id'] == 'pressure':
                pressure_max_values.append(unit.string)
                break
for unit in b.find_all(class_='mint'):
    for parent in unit.parents:
        if parent and 'data-widget-id' in parent.attrs:
            if parent.attrs['data-widget-id'] == 'forecast':
                forecast_min_values.append(unit.string.replace('−', '-'))
                break
            if parent.attrs['data-widget-id'] == 'pressure':
                pressure_min_values.append(unit.string)
                break

weather_labels = [unit.attrs['data-text'] for unit in b.find_all('span', class_='tooltip')]
wind_direction = [unit.string.strip() for unit in b.find_all(class_='w_wind__direction')]
wind_force = [unit.string for unit in b.find_all(class_='js_value val_to_convert')]
wind_max_force = [unit.attrs['data-value'] for unit in b.find_all(class_='w_wind__value widget__value')]
weather_day = [unit.string.strip() for unit in b.find_all(class_='w_date__date')][:10]

weather = pd.DataFrame(
    {
        "period": weather_day,
        "short desc": weather_labels,
        "temp max": forecast_max_values,
        "temp min": forecast_min_values,
        "press max": pressure_max_values,
        "press min": pressure_min_values,
        "wind direction": wind_direction,
        "wind force": wind_force,
        "wind max force": wind_max_force
    }
)
print(weather)
with open('out.html', 'w', encoding='utf-8') as f:
    f.write(weather.to_html(index=False))
