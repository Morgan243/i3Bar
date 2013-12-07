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

        self.current_color = "#bb1111"

        self.poll_error = False

    def setColors(self):
        if self.current_price > self.avg_price:
            self.current_color = "#11bb11"

    def getBTC_price(self):
        try:
            weightedprices_url= "http://api.bitcoincharts.com/v1/weighted_prices.json"
            weightedprices = urlopen(weightedprices_url)
            weightedprices = json.loads(weightedprices.read())
            weighted_24 = float(weightedprices["USD"]["24h"])

            currentprices_url = "https://www.bitstamp.net/api/ticker/"
            currentprices = urlopen(currentprices_url)
            currentprices = json.loads(currentprices.read())
            currentprice = float(currentprices["last"])

            color = 0 # red
            self.current_price = currentprice
            self.avg_price = weighted_24

        except:
            #return "ERROR"
            self.poll_error = True

    def run(self):
        while self.done is not True:
            self.getBTC_price()
            time.sleep(self.poll_interval)

