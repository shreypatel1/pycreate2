import serial
import time

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
    #roombaGPS.append(location)
    time.sleep(1)