'''
py-weather Script
by zeroinfininity2

A weather script to pull weather data for rainmeter
'''

import json
import datetime
import time
import csv
import subprocess
import configparser
import os
import requests
from progressbar import ProgressBar


class Weather:
    '''
    Main class to define a weather object.
    '''
    def __init__(self, config):
        # Initialize the class variables
        self.update_time = int(config['update_time'])
        self.ipaddress = str(config['ipaddress'])
        self.export_csv = config['export_csv']
        self.rainmeter_ctrl = config['rainmeter_ctrl']
        self.current_epoch = int(round(time.time()))
        self.current_hour = int(datetime.datetime.now().strftime('%H'))
        self.weekday = int(datetime.datetime.now().strftime('%w'))
        self.rmcommand = r'Start-Process -FilePath "C:\Program Files\Rainmeter\Rainmeter.exe" -ArgumentList'
        self.scale = None
        self.location = None
        self.weather_data = None
        self.weather_request = None
        self.current = {}
        self.weekly = []
        self.pbar = ProgressBar().start()
        self.debug_message(14)

        # Determine the measurement scale
        match config['preferred_scale']:
            case 'imperial':
                self.scale = {
                    "Temp": "fahrenheit",
                    "Wind": "mph",
                    "Precip": "inch",
                    "Dist": "miles",
                    "Symbol": "˚F"
                }
                self.debug_message(15)
            case _:
                self.scale = {
                    "Temp": "celsius",
                    "Wind": "kmh",
                    "Precip": "mm",
                    "Dist": "km",
                    "Symbol": "˚C"
                }
                self.debug_message(16)
        self.debug_message(17)

    def fetch_ip(self):
        '''
        Fetches the ip address and location values.
        '''
        try:
            get_location = requests.get(
                f"http://ip-api.com/json/{self.ipaddress}?fields=country,region,regionName,city,zip,lat,lon,timezone,isp,org,query").json()

            self.location = {
                'country': get_location['country'],
                'state': get_location['regionName'],
                'city': get_location['city'],
                'latitude': get_location['lat'],
                'longitude': get_location['lon']
            }
            self.debug_message(0)
            return self.location

        except requests.exceptions.RequestException:
            self.debug_message(1)

    def fetch_weatherdata(self):
        """
        Fetches all the weather data and processes the API.
        Caches the data in json.
        """
        try:
            # Try to open the weather data cache
            with open(os.path.join(os.path.dirname(__file__), 'weather_cache.json'), 'r') as file:
                self.weather_data = json.load(file)
                self.debug_message(2)

            # Clear the old weather data if it is older than the update time interval
            # The "current weather" also shows what time the data was last pulled.
            _cached_epoch = int(self.weather_data['current_weather']['time'])
            if self.current_epoch - _cached_epoch >= self.update_time:
                self.weather_data = None
                self.debug_message(3)

        except (FileNotFoundError, json.JSONDecodeError):
            self.debug_message(4)
            self.weather_data = None

        if self.weather_data is None:
            self.debug_message(5)

            # Attempt to get the weather data from the public API
            try:
                self.weather_request = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={self.location['latitude']}&longitude={self.location['longitude']}&current_weather=true&temperature_unit={self.scale['Temp']}&hourly=temperature_2m,relativehumidity_2m,visibility,apparent_temperature,windspeed_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit={self.scale['Temp']}&windspeed_unit={self.scale['Wind']}&precipitation_unit={self.scale['Precip']}&timeformat=unixtime&timezone=auto").json()
            except requests.exceptions.RequestException:
                self.debug_message(6)

            # Create the cache / read
            with open(os.path.join(os.path.dirname(__file__), 'weather_cache.json'), 'w+') as file:
                json.dump(self.weather_request, file, indent=6)
                self.debug_message(7)
                file.seek(0)  # Returns to the start of the file.
                self.weather_data = json.load(file)
                self.debug_message(2)
        return self.weather_data

    def parse_current_weather(self):
        """
        Pulls the current weather from the data.
        """
        self.current = {
            "temperature": self.weather_data["current_weather"]["temperature"],
            "windspeed": self.weather_data["current_weather"]["windspeed"],
            "winddirection": self.weather_data["current_weather"]["winddirection"],
            "weathercode": self.weather_data["current_weather"]["weathercode"],
            "rel_humidity": self.weather_data["hourly"]["relativehumidity_2m"][self.current_hour],
            "visibility": self.weather_data["hourly"]["visibility"][self.current_hour],
            "feels_like": self.weather_data["hourly"]["apparent_temperature"][self.current_hour],
            "maxtemp": self.weather_data["daily"]["temperature_2m_max"][0],
            "mintemp": self.weather_data["daily"]["temperature_2m_min"][0],
            "total_precip": self.weather_data["daily"]["precipitation_sum"][0]
        }
        self.debug_message(8)
        return self.current

    def parse_weekly_forecast(self):
        '''
        Pulls the weekly forecast from the data.
        '''
        weekdays = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
        for day in range(7):
            self.weekly.append(
                {
                    "day": day + 1,
                    'maxtemp': self.weather_data['daily']['temperature_2m_max'][day],
                    'mintemp': self.weather_data['daily']['temperature_2m_min'][day],
                    'weathercode': self.weather_data['daily']['weathercode'][day],
                    'precipitation': self.weather_data['daily']['precipitation_sum'][day],
                    'weekday': weekdays[(self.weekday + day) % 7]
                }
            )
        self.debug_message(9)
        return self.weekly

    def export(self):
        '''
        Exports a CSV of the current weather and the weather forecast.
        Useful for exporting to other programs.
        '''
        if self.export_csv == 'True':
            with open(os.path.join(os.path.dirname(__file__), 'weathercurrent.csv'), 'w') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'temperature',
                    'windspeed',
                    'winddirection',
                    'weathercode',
                    'rel_humidity',
                    'visibility',
                    'feels_like',
                    'maxtemp',
                    'mintemp',
                    'total_precip'
                ])
                writer.writeheader()
                writer.writerow({
                    "temperature": self.current["temperature"],
                    "windspeed": self.current["windspeed"],
                    "winddirection": self.current["winddirection"],
                    "weathercode": self.current["weathercode"],
                    "rel_humidity": self.current["rel_humidity"],
                    "visibility": self.current["visibility"],
                    "feels_like": self.current["feels_like"],
                    "maxtemp": self.current["maxtemp"],
                    "mintemp": self.current["mintemp"],
                    "total_precip": self.current["total_precip"]
                })

            with open(os.path.join(os.path.dirname(__file__), 'weatherforecast.csv'), 'w') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "day",
                    "maxtemp",
                    "mintemp",
                    "weathercode",
                    "precip"
                ])
                writer.writeheader()

                for day in self.weekly:
                    writer.writerow({
                        'day': day['day'],
                        'maxtemp': day['maxtemp'],
                        'mintemp': day['mintemp'],
                        'precip': day['precipitation']
                    })
            self.debug_message(10)

    def rainmeter_controller(self):
        '''
        Sends command line instructions to update the rainmeter skin
        "zerflatUI".
        '''
        if self.rainmeter_ctrl == 'True':
            self.debug_message(12)
            __steps = 18
            try:
                # Update Location Variables
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","country","`"{self.location["country"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((1 / __steps) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","state","`"{self.location["state"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((2 / __steps) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","city","`"{self.location["city"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((3 / __steps) * 100)

                # Update Scale variables
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","temp_symbol","`"{self.scale["Symbol"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((4 / __steps) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","ws_unit","`"{self.scale["Wind"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((5 / __steps) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","precip_unit","`"{self.scale["Precip"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((6 / __steps) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","dist_unit","`"{self.scale["Dist"]}`"","zeroflatUI\\weather"'])
                self.pbar.update((7 / __steps) * 100)

                # Update Current weather variables
                for key in self.current:
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","current_{key}","{self.current[f"{key}"]}","zeroflatUI\\weather"'])
                self.pbar.update((8 / __steps) * 100)

                # Update the time of day
                nightday = 'day' if 18 > self.current_hour >= 6 else 'night'
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","nightday","{nightday}","zeroflatUI\\weather"'])
                self.pbar.update((9 / __steps) * 100)

                # Update Forecast Variables
                for daily in self.weekly:
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","day{daily["day"]}_maxtemp","{daily[f"maxtemp"]}","zeroflatUI\\weather"'])
                    self.pbar.update((10 / __steps) * 100)
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","day{daily["day"]}_mintemp","{daily[f"mintemp"]}","zeroflatUI\\weather"'])
                    self.pbar.update((11 / __steps) * 100)
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","day{daily["day"]}_weathercode","{daily[f"weathercode"]}","zeroflatUI\\weather"'])
                    self.pbar.update((12 / __steps) * 100)
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","day{daily["day"]}_precip","{daily[f"precipitation"]}","zeroflatUI\\weather"'])
                    self.pbar.update((13 / __steps) * 100)
                    subprocess.run(['powershell.exe', f'{self.rmcommand} "!SetVariable","day{daily["day"]}_weekday","{daily[f"weekday"]}","zeroflatUI\\weather"'])
                    self.pbar.update((14 / __steps) * 100)

                # Redraw Rainmeter and enable
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!EnableMeasureGroup", "WeatherGroup","zeroflatUI\\weather"'])
                self.pbar.update((15 / 18) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!UpdateMeasureGroup", "WeatherGroup","zeroflatUI\\weather"'])
                self.pbar.update((16 / 18) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!UpdateMeter", "*","zeroflatUI\\weather"'])
                self.pbar.update((17 / 18) * 100)
                subprocess.run(['powershell.exe', f'{self.rmcommand} "!Redraw","zeroflatUI\\weather"'])
                self.pbar.update((18 / 18) * 100)
                self.pbar.finish()
                self.debug_message(13)
            except Exception as e:
                self.debug_message(18)

    def fetch_all(self):
        '''
        This function calls all of the other functions.
        '''
        self.fetch_ip()
        self.fetch_weatherdata()
        self.parse_current_weather()
        self.parse_weekly_forecast()

    def debug_message(self, index):
        '''
        An index of the debug messages. Returns the message to the console if set to true.
        '''
        self.debug_messages = (
            'Successfully fetched location...',
            'Unable to fetch location! Check your internet connection...',
            'Fetched data from local cache...',
            'Older weather data cleared...',
            'No local cache found!',
            'Fetching new json data!',
            'There was an error fetching your api request. Check if the api is working or the location is correct. Attempting to read from cache...',
            'Success writing to cache!',
            'Current weather successfully parsed from cache...',
            'Weekly weather successfully parsed from cache...',
            'Weather data sucessfully exported to CSV...',
            'Failed to export CSV. Check your API request.',
            'Updating Rainmeter...',
            'Rainmeter sucessfully updated...',
            'Alert! Debug Mode enabled... ',
            'Measurement scale set to imperial...',
            'Measurement scale set to metric...',
            'Config successfully loaded...',
            'Unable to update Rainmeter. Ensure you are using zeroflatUI, and Rainmeter is running.'
        )
        return print(self.debug_messages[index])


def read_config(file_path):
    '''
    Reads the config file and passes in the values to the script.
    '''
    c_values = {}
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            c_values.update({key: config[section][key]})
    return c_values


def main():
    config = read_config(os.path.join(os.path.dirname(__file__), 'pyweather_config.ini'))
    forecast = Weather(config)
    forecast.fetch_all()
    forecast.export()
    forecast.rainmeter_controller()


if __name__ == '__main__':
    main()
