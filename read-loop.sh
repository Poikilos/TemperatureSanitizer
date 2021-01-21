#!/bin/bash
CMD=./readTEMPer-driverless-withdate.sh
if [ ! -f "`command -v hid-query`" ]; then
    CMD=./get_temp.sh
fi

while [ true ]; do
    temp=`$CMD`
    if [ $? -ne 0 ]; then
        echo "$CMD did not work: $temp"
        exit 1
    else
        echo $(date +"%F %T") " , " $temp
        sleep 60
    fi
done
