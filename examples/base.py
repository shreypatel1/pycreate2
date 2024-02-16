import serial
import socket

ser = serial.Serial('/dev/tty.usbmodem12401', 9600)
host = '10.100.139.104'  # Node B's IP address
port = 4055  # Port for communication
sAddr = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print('Connected to {}:{}'.format(host, port))

while True:
    try:
        line = ser.readline()

        # bind socket and send data
        # sock.sendall(line)
        print(line.decode('utf-8'))
        server_socket.sendto(line, sAddr)
    except KeyboardInterrupt:
        server_socket.close()
        break