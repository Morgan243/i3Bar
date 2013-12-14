from urllib import urlopen
import sys
import json
import time
import threading

class WeatherMon(threading.Thread):
    def __init__(self, location='Richmond,va'):
        threading.Thread.__init__(self)
        self.daemon = True
        self.done = False

        self.poll_interval = 150 

        self.location = location
        self.state = location.split(',')[1]
        self.city = location.split(',')[0]
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q=' + self.city +',' + self.state


        self.color = "#555555"
        self.weather_string = "Updating..."

        self.temp_min = 0.0
        self.temp_max = 0.0
        self.temp = 0.0
        self.wind = 0.0
        self.weather_main = "Fine"
        self.weather_desc = "Fine"

#---- Example JSON -----
#{"coord":{"lon":-77.43,"lat":37.54},"sys":{"message":0.0063,"country":"United States of America","sunrise":1386504756,"sunset":1386539486},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"base":"gdps stations","main":{"temp":274.9,"pressure":1033,"temp_min":273.71,"temp_max":276.15,"humidity":71},"wind":{"speed":3.26,"deg":17.0015},"rain":{"3h":0},"clouds":{"all":64},"dt":1386471173,"id":4781708,"name":"Richmond","cod":200}
    def getWeather(self):
        try:
            self.weather_raw = urlopen(self.url)
            self.weather_json = json.loads(self.weather_raw.read())

            self.temp_min = float(self.weather_json["main"]["temp_min"])
            self.temp_max = float(self.weather_json["main"]["temp_max"])
            self.temp = float(self.weather_json["main"]["temp"])

            self.weather_desc = str(self.weather_json["weather"][0]["description"])

            #self.weather_string = str( ((self.temp_max + self.temp_min)/2.0) - 273.0 ) + 'C'
            self.weather_string = str( self.temp - 273.0 ) + 'C'
            self.weather_string = self.weather_string + " - " + self.weather_desc
            self.color = "#555555"
        except:
            self.weather_string = "ERROR Fetching Weather!"
            self.color = "#663333"

    def run(self):
        while self.done is not True:
            self.getWeather()
            time.sleep(self.poll_interval)
            
