This code was created from 'wrapper.py' that currently (12-2013)
exists here:
http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.py

i3 statusbar wrapper script which currently...
  -> Removes any items that don't have values (have 'no' or 'down')

  - Monitors the Price of BTC in a second thread
      - Outputs '[BTC<indicators>] $<24h_average_price> ($<current_price)'
          - Indicators are a string of '-' (for below avg.) and '+' (above avg.)
          with the string gaining an indicator every hour it is above/below.
          - A '~' will prepend the output if there is an error fetching the pricing data.
          The output will remain as the last values retrieved and indicators will not update.  


**Usage**

  1.) Make sure you have a status bar config. Copy the default from /etc/i3status.conf (may
      vary depending on distro). Doesn't matter you put it (maybe ~/.i3/i3status.conf).
  
  2.) Make sure the 'general' section at the top of i3status.conf has the following:
              - output_format = "i3bar"
              - colors = true
  
  3.) Change the 'bar' section in the i3 configuration file (usually in ~/.i3/config) to:
              - status_command i3status -c /path/to/i3status.conf | /path/to/stat_wrap.py
  
  4.) You can restart i3 in place using Mod+Shift+r (mod is typically alt or windoze key)
  
  5.) Enjoy
