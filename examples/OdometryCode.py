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
import turtle as t


if __name__ == "__main__":
    ws = t.Screen()
    botExample = t.Turtle()
    fontStyle = ("Arial", 17, "bold")

    # Create a Create2 Bot
    port = '/dev/tty.usbserial-DN026AEG'
    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = pycreate2.Create2(port=port, baud=baud['default'])

    # define a movement path
    '''
    [ 200, 200, 3, 'for'],
    [-200,-200, 3, 'back'],
    [   0,   0, 1, 'stop'],
    [ 100,   0, 2, 'rite'],
    [   0, 100, 4, 'left'],
    [ 100,   0, 2, 'rite'],
    [   0,   0, 1, 'stop']

    [ 130, 130, 3, 'for'],
    [ 0,   -185, 2, 'left'],
    [   0,   0, 1, 'stop'],
    [ 130, 130, 3, 'for'],
    [ 0,   -185, 2, 'left'],
    [   0,   0, 1, 'stop'],
    [ 130, 130, 3, 'for'],
    [ 0,   -185, 2, 'left'],
    [   0,   0, 1, 'stop'],
    [ 130, 130, 3, 'for'],
    [ 0,   -185, 2, 'left'],
    [   0,   0, 1, 'stop']
    '''
    path = [

        [ 130, 130, 3, 'for']
    ]

    bot.start()
    bot.safe()
    tickList = []
    initialEncoder = []
    finalEncoder = []

    #~600 tick per revolution
    #282mm for one revolution
    #0.47mm per tick

    #Don't do goto because it's not accurate
    #use forward, backward, right, left so that the coordinate values
    #can properly stack and not reset when using the "goto" method

    #possible formulas needed: slope formula

    # path to move
    while (True):
        #sensors = bot.get_sensors()
        for lft, rht, dt, s in path:
            sensors = bot.get_sensors()
            initialEncoder = [sensors.encoder_counts_left, sensors.encoder_counts_right]
            leftEM = sensors.encoder_counts_left
            rightEM = sensors.encoder_counts_right
            print("LEFT MOTOR VALUE: {} RIGHT MOTOR VALUE: {}".format(leftEM, rightEM))
            
            if (lft == rht):
                #botExample.speed(dt)
                botExample.forward(lft)
                
            else:
                #botExample.speed(dt)
                lft_turn = (rht * -1) - 95; rht_turn = (lft * -1) - 95
                print("LEFT TURN VALUE: {} RIGHT TURN VALUE: {}".format(lft_turn, rht_turn))
                if lft != 0:
                    botExample.left(lft_turn)

                if rht != 0:
                    botExample.right(rht_turn)
            
            print("MY POSITION")
            botExample.write(botExample.position(), font=fontStyle)
            botExample.ht(); botExample.stamp(); botExample.st()
            print(lft, rht)
            print(s)
            bot.digit_led_ascii(s)

            
            
            bot.drive_direct(lft, rht)
            time.sleep(dt)

            sensors = bot.get_sensors()
            finalEncoder = [sensors.encoder_counts_left, sensors.encoder_counts_right]
            leftEM = sensors.encoder_counts_left
            rightEM = sensors.encoder_counts_right
            print("LEFT MOTOR VALUE: {} RIGHT MOTOR VALUE: {}".format(leftEM, rightEM))

            print(finalEncoder[0])
            print(initialEncoder[0])
            leftDiff = (finalEncoder[0] - initialEncoder[0])
            rightDiff = (finalEncoder[1] - initialEncoder[1])

            difference = [leftDiff, rightDiff]
            tickList.append(difference)
            print("TICK LIST: ", tickList)



    print('shutting down ... bye')
    bot.drive_stop()
    time.sleep(0.1)

    ws.mainloop()