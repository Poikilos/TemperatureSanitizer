#!/bin/bash

EXTRA_GET_TEMP_ARGS=

usage(){
    cat <<END

Usage:
-f: display the temperature in fahrenheit

END
}

ANY_ARGS=false

for var in "$@"
do
    if [ "@$var" = "@-f" ]; then
        EXTRA_GET_TEMP_ARGS="$EXTRA_BAD_TEMP_ARGS -f"
    else
        echo "unknown argument: $var"
        usage
        exit 1
    fi
    ANY_ARGS=true
done


CMD=./readTEMPer-driverless-withdate.sh
if [ ! -f "`command -v hid-query`" ]; then
    CMD="./get_temp.sh --silent-if-ok $EXTRA_GET_TEMP_ARGS"
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
