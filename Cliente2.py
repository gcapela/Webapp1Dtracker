# Cliente que envia dados

import socket
import time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9999)

print('connecting to ' + str(server_address[0]) + ' port ' + str(server_address[1]))
tcp.connect(server_address)

while True:

    msg = '11 , 1.64 , 35'

    print('sending -->  ' + msg)
    tcp.send(msg.encode())
    time.sleep(10)

tcp.close()
