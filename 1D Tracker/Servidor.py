# Servidor que recebe os dados

import socket
import time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 10000)

print ('starting up on ' + str(server_address[0]) + ' port ' + str(server_address[1]))
tcp.bind(server_address)

tcp.listen(10)

print ('waiting for a connection... ')
con, client_address = tcp.accept()
    
while True:
    
    print ('connected with ' + str(client_address))

    msg = con.recv(1024)
    print ('received ' + msg)


print('closing connection')
con.close()              
