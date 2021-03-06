![](screen_shot.png)

i3 status bar (*i3status*) wrapper script which currently...

  - Removes any items that don't have values (have 'no' or 'down')

  - Monitors the Price of BTC in a second thread
      - Enable with '-b'
      - Outputs **[BTC<indicators>] $24h_average_price ($current_price)**
          - Indicators are a string of '-' (for below avg.) and '+' (above avg.)
          with the string gaining an indicator every hour it is above/below.
          - A '~' will prepend the output if there is an error fetching the pricing data.
          The output will remain as the last values retrieved and indicators will not update.  

  - Outputs the weather for a Open Weather Map compatible location
        - Use the '-w' option to select a location


**Usage**

    Usage: stat_wrap.py [options]

    Options:
      -h, --help            show this help message and exit
      -w WEATHER_URI, --weather-location=WEATHER_URI
                            Comma delimited city and state (city,state) for
                            openweathermap json api
      -b, --bitcoin-monitor
                            Get BTC prices from bitcoincharts and bitstamp 

*1.)* Make sure you have a status bar config. Copy the default from /etc/i3status.conf (may
      vary depending on distro). Doesn't matter where you put it (maybe ~/.i3/i3status.conf).
  
*2.)* Make sure the 'general' section at the top of i3status.conf has the following:

    output_format = "i3bar"
    colors = true
 

*3.)* Change the 'bar' section in the i3 configuration file (usually in ~/.i3/config) to:

    status_command i3status -c /path/to/i3status.conf | /path/to/stat_wrap.py -w Richmond,va -b


*4.)* You can restart i3 in place using Mod+Shift+r (mod is typically alt or windoze key)
  
*5.)* Enjoy

This code was created from 'wrapper.py' that currently (12-2013)
exists here:
http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.py
