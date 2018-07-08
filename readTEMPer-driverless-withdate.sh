#!/bin/bash
OUTLINE=`sudo hid-query /dev/hidraw1 0x01 0x80 0x33 0x01 0x00 0x00 0x00 0x00|grep -A1 ^Response|tail -1`
echo $OUTLINE
OUTNUM=`echo $OUTLINE|sed -e 's/^[^0-9a-f]*[0-9a-f][0-9a-f] [0-9a-f][0-9a-f] \([0-9a-f][0-9a-f]\) \([0-9a-f][0-9a-f]\) .*$/0x\1\2/'`
HEX4=${OUTNUM:2:4}
DVAL=$(( 16#$HEX4 ))
# scale is # of decimal places, and original value is int so divide by 100 to get real value
bc <<< "scale=2; $DVAL/100"
