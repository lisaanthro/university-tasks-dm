import requests


class ForecastApi:
    api_key: str = '853f4168e066455c96284920230310'
    forecast_url: str = 'http://api.weatherapi.com/v1/forecast.json'

    def get_forecast(self, city: str, days=1):
        response = requests.get(self.forecast_url, params={
            'key': self.api_key,
            'q': city,
            'days': days,
            'lang': 'ru'
        })
        print(city, days)
        print(response.json())
        if 'error' in response.json():
            raise ValueError
        data = response.json()['forecast']['forecastday']
        print(f'{data=}')
        return self._clear_data(data)

    @staticmethod
    def _clear_data(data):
        forecast_message = f''
        for day in data:
            day_string = f"{day['date']}\tМин. {day['day']['mintemp_c']}°C Макс. {day['day']['maxtemp_c']}°C \n{day['day']['condition']['text']}"
            forecast_message += day_string + '\n'
        return forecast_message
