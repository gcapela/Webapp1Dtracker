# Cliente que envia dados

import socket
import time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9999)

print('connecting to ' + str(server_address[0]) + ' port ' + str(server_address[1]))
tcp.connect(server_address)

while True:

    mensagens = ('12 , 1.64 , 40 , 0.27', '13 , 1.24 , 39 , 0.30', '15 , 1.45 , 42 , 0.5', '11 , 2.00 , 41 , 0.22', '16 , 1.33 , 42 , 0.43')

    for msg in mensagens:

        print('sending -->  ' + msg)
        tcp.send(msg.encode())
        time.sleep(5)

tcp.close()
