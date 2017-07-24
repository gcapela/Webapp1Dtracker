# Versão 2.0 - 20/07/2017
# Cliente que envia dados

import socket
import time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9999)

print('connecting to ' + str(server_address[0]) + ' port ' + str(server_address[1]))
tcp.connect(server_address)

while True:

    msg = '12 , 1.64 , 40, 0.27'

    print('sending -->  ' + msg)
    tcp.send(msg.encode())
    time.sleep(10)

    msg = '10 , 1.50 , 35, 0.40'

    print('sending -->  ' + msg)
    tcp.send(msg.encode())
    time.sleep(10)

    msg = '15 , 2.00 , 42, 0.50'

    print('sending -->  ' + msg)
    tcp.send(msg.encode())
    time.sleep(10)

tcp.close()
