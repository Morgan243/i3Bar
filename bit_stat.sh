#!/bin/bash


i3status -c ~/.i3/.i3status.conf | while read status
do
    
    echo "BTC = \$`poll_btc` | $status"
done
