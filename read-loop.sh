#!/bin/bash
while [ true ]; do
  temp=`./readTEMPer-driverless-withdate.sh`
  echo $(date +"%F %T") " , " $temp
  sleep 60
done
