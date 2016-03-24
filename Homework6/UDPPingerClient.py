#!/usr/bin/python2.7
import socket
from datetime import datetime


# Address to use
server_address = ('localhost', 12000)

# Initialize a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1.0)
print('\n' * 3 + '/' * 10 + ' Pinging Server ' + '/' * 10 + '\n' * 3)

for d in range(1, 11, 1):

    try:
        message = 'Ping ' + str(d) + ' ' + str(datetime.now().microsecond)
        print('Sending Message: ' + message)
        s.sendto(message, server_address)
        data = s.recv(1024)
        print('Server Response: ' + str(data) + '\n')
        segments = str(data).split()
        RTT = datetime.now().microsecond - int(segments[2])
        print('Ping ' + str(d) + ' RTT: ' + str(RTT) + ' us \n')
    except socket.timeout:
        print('Socket Timed Out In Sequence: ' + str(d) + '\n')


s.close()

