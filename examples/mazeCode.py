#!/usr/bin/env python3
#-*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# moves the roomba through a simple sequence

import pycreate2
import time


if __name__ == "__main__":
    # Create a Create2 Bot
    port = '/dev/tty.usbserial-DN026AEG'  # this is the serial port on my iMac
    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = pycreate2.Create2(port=port, baud=baud['default'])

    # define a movement path
    """path = [
        #[ 200, 200, 3, 'for'],
        #[-200,-200, 3, 'back'],
        #[   0,   0, 1, 'stop'],
        #[ 100,   0, 2, 'rite'],
        #[   0, 100, 4, 'left'],
        #[ 100,   0, 2, 'rite'],
        #[   0,   0, 1, 'stop'],
        ###[ 50,   200, 15, 'rite'],
        [ 200,   200, 4, 'for'],
        [ 0,   200, 2.8, 'left'],
        [ 200,   200, 4, 'for'],
        [ 200,  50, 4, 'rite'],
        [ 200,   200, 4, 'for'],
    ]"""

    bot.start()
    bot.safe()
    print('Starting ...')

    # path to move
    """for lft, rht, dt, s in path:
        print(s)
        bot.digit_led_ascii(s)
        bot.drive_direct(rht, lft)
        time.sleep(dt)
    """


    # detects for any obstacle in front of the robot
    def detectObstacle():
        sensor = bot.get_sensors()
        
        #print("[L ] [LF] [LC] [CR] [RF] [ R]")
        print("[L ]  [C]  [ R]")

        sensorLeft = sensor.light_bumper_left + sensor.light_bumper_front_left
        sensorRight = sensor.light_bumper_right + sensor.light_bumper_front_right
        sensorCenter = sensor.light_bumper_center_left + sensor.light_bumper_center_right

        #print(f"{sensor.light_bumper_left:4} {sensor.light_bumper_front_left:4} {sensor.light_bumper_center_left:4} {sensor.light_bumper_center_right:4} {sensor.light_bumper_front_right:4} {sensor.light_bumper_right:4}")
        print(f"{sensorLeft} {sensorCenter} {sensorRight}")

    # looks for an open way
    def checkSurroundings():
        # iterate through 3 directions to find an open way
        for x in range(3):
            openPath = False

            #check for obstacle and change direction if needed
            if x == 0:
                openPath = not detectObstacle()
            elif x == 1:
                #
                openPath = not detectObstacle()
            elif x == 2:
                #
                openPath = not detectObstacle()

            #check if any open way was detected
            if openPath == True:
                #
                sides = {
                    0: "front",
                    1: "left",
                    2: "right"
                }
                print(sides.get(x, "no direction") + " is open")
            
            #

    
            
        

    gridSize = 0.5 # all values are in meters

    #code to make the robot move 0.5m forward and detect for obstacles


    print('shutting down ... bye')
    bot.drive_stop()
    time.sleep(0.1)
