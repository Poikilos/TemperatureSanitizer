#!/bin/sh

./get_temp.sh --silent-if-ok -f

source ./temper_env.rc

TEMP_RESULT=$?
if [ $TEMP_RESULT -eq 0 ]; then
    source $ACTIVATOR
    #^ from temper_env.rc
fi
python TemperatureSanitizer.py
