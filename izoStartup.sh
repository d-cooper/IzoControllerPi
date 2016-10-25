#!/bin/sh -e

sleep 10
python3 /home/pi/Desktop/IzoControllerPi/IzoControllerPi/IzoControllerPi.py > /home/pi/Desktop/IzoControllerPi/log.txt 2>&1 &

exit 0