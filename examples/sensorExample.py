#!/usr/bin/env python3
#-*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from pycreate2 import Create2
import time


if __name__ == "__main__":
    port = '/dev/tty.usbserial-DN026AEG'
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = Create2(port=port, baud=baud['default'])

    bot.start()

    bot.safe()

    print('Starting ...')

    cnt = 0
    while True:
        # Packet 100 contains all sensor data.
        sensor = bot.get_sensors()

        if cnt%20 == 0:
            #print("[L ] [LF] [LC] [CR] [RF] [ R]")
            print("[L ]  [C]  [ R]")
        
        sensorLeft = sensor.light_bumper_left + sensor.light_bumper_front_left
        sensorRight = sensor.light_bumper_right + sensor.light_bumper_front_right
        sensorCenter = sensor.light_bumper_center_left + sensor.light_bumper_center_right


        #print(f"{sensor.light_bumper_left:4} {sensor.light_bumper_front_left:4} {sensor.light_bumper_center_left:4} {sensor.light_bumper_center_right:4} {sensor.light_bumper_front_right:4} {sensor.light_bumper_right:4}")
        print(f"{sensorLeft} {sensorCenter} {sensorRight}")

        
        #OUTPUT
        if sensorCenter > sensorLeft or sensorCenter > sensorRight:
            if sensorLeft > sensorRight:
                bot.drive_direct(lft, rht)

        time.sleep(.01)

        cnt += 1
