import math
import pycreate2
import time
import serial
import socket

roombaGPS = [
    [0.0, 0.0],
]
baseGPS = [
    [0.0, 0.0],
]
rDirection = 0.0

async def updateBaseGPS():
    # get dog's gps coordinates

    host = '10.101.191.42'  # Node A's IP address
    port = 4050  # Port for communication between base and roomba

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    print('connecting to {} port {}'.format(host, port))
    sock.connect(host, port)

    while True:
        # get dog's gps coordinates
        data = sock.recv(1024)
        data = data.decode('utf-8')
        data = data.split(',')
        latitude = float(data[0])
        longitude = float(data[1])
        location = [longitude, latitude]

        # add gps coordinates to baseGPS list
        baseGPS.append(location)

async def updateRoombaGPS():
    # get roomba's gps coordinates
    ser = serial.Serial('/dev/tty.usbmodem112401', 9600)

    while True:
        # get roomba's gps coordinates
        line = ser.readline().decode('utf-8')
        line = line.split(',')
        latitude = float(line[0])
        longitude = float(line[1])
        location = [longitude, latitude]

        # add gps coordinates to roombaGPS list
        #roombaGPS.append([0,0])
        #time.sleep(1)
        print(location)
        roombaGPS.append(location)
        time.sleep(1)

def calcRoombaDirection():
    # run the set of commands to determine roomba's front direction
    global rDirection

    # get roomba's initial gps coordinates
    iLoc = roombaGPS[roombaGPS.length - 1]

    # drive roomba straight for 1 meter
    print('for')
    bot.digit_led_ascii('for')
    bot.drive_direct(200, 200)
    time.sleep(4)
    bot.drive_stop()

    # get roomba's gps coordinates again
    time.sleep(3)
    fLoc = roombaGPS[roombaGPS.length - 1]

    # compare the two xy format gps coordinates
    dY = fLoc[1] - iLoc[1]
    dX = fLoc[0] - iLoc[0]
    rDirection = math.atan2(dY, dX)
    if rDirection < 0:
        rDirection += 2 * math.pi

def calcTargetRotation():
    # calculate the rotation needed to face the base
    dY = baseGPS[baseGPS.length - 1][1] - roombaGPS[roombaGPS.length - 1][1]
    dX = baseGPS[baseGPS.length - 1][0] - roombaGPS[roombaGPS.length - 1][0]

    target = math.atan2(dY, dX)
    if target < 0:
        target += 2 * math.pi
    rotation = target - rDirection
    if rotation > math.pi:
        rotation -= 2 * math.pi
    elif rotation < -math.pi:
        rotation += 2 * math.pi
    
    return rotation, target

def getDistance():
    # get distance between roomba and base
    dY = baseGPS[baseGPS.length - 1][1] - roombaGPS[roombaGPS.length - 1][1]
    dX = baseGPS[baseGPS.length - 1][0] - roombaGPS[roombaGPS.length - 1][0]
    distance = math.sqrt(dY * dY + dX * dX)

    return distance

def waitForRotation(rotation):
    # calculate the time needed to rotate roomba
    rotation = abs(rotation)
    time = (1.04 / math.pi) * rotation

    return time

def runRoomba():
    # rotate roomba to the target angle
    rotation, target = calcTargetRotation()
    if rotation > 0:
        # rotate roomba clockwise
        print('rite')
        bot.digit_led_ascii('rite')
        bot.drive_direct(-400, 400)
    elif rotation < 0:
        # rotate roomba counter-clockwise
        print('left')
        bot.digit_led_ascii('left')
        bot.drive_direct(400, -400)

    waitForRotation(rotation)
    
    bot.drive_stop()
    # Update rDirection with target
    global rDirection
    rDirection = target


    # drive roomba straight until it is in 0.5 meter range from the base
    distance = getDistance()
    if distance > 0.5:
        # drive roomba
        print('for')
        bot.digit_led_ascii('for')
        bot.drive_direct(200, 200)

    while distance > 0.5:
        # drive roomba
        distance = getDistance()
        time.sleep(0.2)

    # stop roomba
    bot.drive_stop()
    print('reached base')
        


if __name__ == "__main__":
    # Create a Create2 Bot
    port = '/dev/tty.usbserial-DN026AEG'  # this is the serial port on my iMac
    # port = '/dev/ttyUSB0'  # this is the serial port on my raspberry pi
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }

    bot = pycreate2.Create2(port=port, baud=baud['default'])
    bot.start()
    bot.safe()

    # start GPS update async functions
    updateBaseGPS()
    updateRoombaGPS()


    # find roomba's direction
    calcRoombaDirection()

    # run roomba follower program
    try:
        runRoomba()
    except KeyboardInterrupt:
        bot.drive_stop()
        time.sleep(0.1)


    # shut down
    print('shutting down ... bye')
    bot.drive_stop()
    time.sleep(0.1)
