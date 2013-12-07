#!/usr/bin/python2
from urllib import urlopen
import sys
import json
import time
from bit_mon import BTCMon

btc_mon = BTCMon()

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
        btc_mon.done = True
        btc_mon.join()

def cleanUp(j):
    found = True
    while found:
        found = False
        for i in xrange(len(j)):
            if "no" in j[i]["full_text"] or "down" in j[i]["full_text"]:
                j.pop(i)
                found = True
                break
                

if __name__ == '__main__':
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

        # insert information into the start of the json, but could be anywhere
        if btc_mon.poll_error:
            j.insert(0, {'full_text' : '~[BTC%s] $%s ($%s)' 
                % (btc_mon.indicators, btc_mon.avg_price, btc_mon.current_price), 
                'name' : 'btc', 'color' : btc_mon.current_color})
        else:
            j.insert(0, {'full_text' : '[BTC%s] $%s ($%s)' 
                % (btc_mon.indicators, btc_mon.avg_price, btc_mon.current_price), 
                'name' : 'btc', 'color' : btc_mon.current_color})
        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
