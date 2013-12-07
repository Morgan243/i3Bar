from urllib import urlopen
import sys
import json
import time
import threading

class BTCMon(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True
        self.done = False
        self.poll_interval = 5
        self.current_price = 0
        self.avg_price = 0

        self.price_rat = 0.0
        self.current_color = "#bb1111"

        self.poll_error = False
        self.indicators = ''
        #add '+' or '-' for every hour it is above/below the average
        self.tick_time = 3600.0
        self.count_to_tick = self.tick_time/self.poll_interval
        self.up_count = 0
        self.down_count = 0

    def setIndicator(self):
        if self.price_rat > 1.0:
            self.up_count += 1
            self.down_count = 0
            ticks = self.up_count/self.count_to_tick
            self.indicators = "+" * int(ticks)

        elif self.price_rat < 1.0:
            self.up_count = 0
            self.down_count += 1

            ticks = self.down_count/self.count_to_tick
            self.indicators = "-" * int(ticks)
        

        

    def setColors(self):
        self.price_rat = float(self.current_price) / float(self.avg_price)

        if self.price_rat > 1.0:
            if self.price_rat < 1.001:
                self.current_color = "#117f11"
            elif self.price_rat < 1.01:
                self.current_color = "#119011"
            elif self.price_rat < 1.1:
                self.current_color = "#119b11"
            elif self.price_rat < 1.2:
                self.current_color = "#01ab01"

        else:
            if self.price_rat > .99:
                self.current_color = "#7f1111"
            elif self.price_rat > .98:
                self.current_color = "#901111"
            elif self.price_rat > .95:
                self.current_color = "#b01111"

    def getBTC_price(self):
        try:
            #this code courtesy some other fella on GitHub
            weightedprices_url= "http://api.bitcoincharts.com/v1/weighted_prices.json"
            weightedprices = urlopen(weightedprices_url)
            weightedprices = json.loads(weightedprices.read())
            weighted_24 = float(weightedprices["USD"]["24h"])

            currentprices_url = "https://www.bitstamp.net/api/ticker/"
            currentprices = urlopen(currentprices_url)
            currentprices = json.loads(currentprices.read())
            currentprice = float(currentprices["last"])

            #prices we are interested in
            self.current_price = currentprice
            self.avg_price = weighted_24

            self.poll_error = False

        except:
            self.poll_error = True

    def run(self):
        while self.done is not True:
            self.getBTC_price()
            if self.poll_error is not True:
                self.setColors()
                self.setIndicator()
            time.sleep(self.poll_interval)

