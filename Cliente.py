# Cliente que envia dados random

import socket
import time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print ('connecting to ' + str(server_address[0]) + ' port ' + str(server_address[1]))
tcp.connect(server_address)

while True:
    
    msg = 'mensagem de teste'
    
    print ('sending -->  ' + msg)
    tcp.send(msg)
    time.sleep(10)
        
tcp.close()