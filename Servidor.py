# Servidor que recebe os dados

import socket
import _thread

dados = {}

# ---------------------------------Threads----------------------------------- #


def read(conn, client_address):

    while True:

        msg = conn.recv(1024)

        if not msg:
            print('no message received')
            break

        print('received -->  ' + msg.decode())

        if msg.decode() == 'close':
            break

        global dados

        if str(client_address[0]) not in dados.keys():

            dados[str(client_address[0])] = [(float(msg.decode().split(',')[0]), float(
                msg.decode().split(',')[1]), float(msg.decode().split(',')[2]))]

        else:

            dados[str(client_address[0])] += [(float(msg.decode().split(',')[0]),
                                               float(msg.decode().split(',')[1]), float(msg.decode().split(',')[2]))]

        print('dados ---> ' + str(dados))

    conn.close()
    print(str(client_address) + ' - closed connection')
    _thread.exit()

#############################################################################


def connect():

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('', 9999)

    print('starting up on ' +
          str(server_address[0]) + ' port ' + str(server_address[1]))
    tcp.bind(server_address)

    tcp.listen(10)

    print('waiting for a connection... ')

    while True:

        (conn, client_address) = tcp.accept()
        print('connected with ' + str(client_address))

        _thread.start_new_thread(read, (conn, client_address))

    _thread.exit()

# --------------------------------------------------------------------------- #


_thread.start_new_thread(connect, ())

while True:
    pass
