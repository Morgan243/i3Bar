#!/usr/bin/python2
from urllib import urlopen
import json
import time
#from beautifulhue.api import Bridge

# CONFIGURE HERE
#bridge = Bridge(device={'ip':'192.168.1.28'}, user={'name': 'newdeveloper'})
#light_id = 1

#while True:
#active_light = bridge.light.get({'which': light_id})
previous_color = -1
#if active_light['resource']['state']['on']:
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

    print str(currentprice)
except:
    print "ERROR"
#        if currentprice > weighted_24:
#            color = 25500 # green
#        if color != previous_color:
#            bridge.light.update({'which': light_id, 'data': {'state': {'hue': color}}})
#            previous_color = color
#            print "updating light color -- current=%s, avg=%s" % (currentprice, weighted_24)
#
    #time.sleep(60 * 1000)
