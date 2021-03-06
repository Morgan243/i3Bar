#!/usr/bin/python2
from urllib import urlopen
import sys
import json
import time
from bit_mon import BTCMon
from weather_mon import WeatherMon    
from optparse import OptionParser



def get_governor():
    """ Get the current governor for cpu0, assuming all CPUs use the same. """
    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor') as fp:
        return fp.readlines()[0].strip()

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

def cleanUp(j):
    found = True
    while found:
        found = False
        for i in xrange(len(j)):
            text = j[i]["full_text"]
            if "no" in text or "down" in text  or "No battery" in text:
                j.pop(i)
                found = True
                break
                

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-w", "--weather-location", dest="WEATHER_URI",
                        help="Comma delimited city and state (city,state) for openweathermap json api")

    parser.add_option("-b", "--bitcoin-monitor", dest="BTC_ON", default=False, action="store_true",
                        help="Get BTC prices from bitcoincharts and bitstamp")

    (options, args) = parser.parse_args()

    weath_mon = None
    btc_mon = None

    if options.WEATHER_URI is not None:
        weath_mon = WeatherMon(options.WEATHER_URI)
        weath_mon.start()
    if options.BTC_ON:
        btc_mon = BTCMon()
        btc_mon.start()

    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','


        j = json.loads(line)

        cleanUp(j)


        if btc_mon is not None:
            # insert information into the start of the json, but could be anywhere
            if btc_mon.poll_error:
                j.insert(0, {'full_text' : '~[BTC%s] $%s ($%s)' 
                    % (btc_mon.indicators, btc_mon.avg_price, btc_mon.current_price), 
                    'name' : 'btc', 'color' : btc_mon.current_color})
            else:
                j.insert(0, {'full_text' : '[BTC%s] $%s ($%s)' 
                    % (btc_mon.indicators, btc_mon.avg_price, btc_mon.current_price), 
                    'name' : 'btc', 'color' : btc_mon.current_color})


        #insert weather if it is desired
        if weath_mon is not None:
            j.insert(0, {'full_text' : '%s' % weath_mon.weather_string, 'name' : 'weather', 
                    'color' : weath_mon.color})

        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
