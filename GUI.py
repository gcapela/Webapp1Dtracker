# ######################################################################### #
# ############################## Servidor ################################# #
# ######################################################################### #

import socket
import _thread
from tkinter import *

dados = {}

new_data = 0

# --------------------------------Threads---------------------------------- #
# TODO: meter o msg.decode().split(',') numa variavel?


def read(conn, client_address):

    while True:

        msg = conn.recv(1024)

        if not msg:
            print('no message received')
            break

        print('received -->  ' + msg.decode())

        if msg == 'close':
            break

        global dados

        if str(client_address[0]) not in dados.keys():

            dados[str(client_address[0])] = [(float(msg.decode().split(',')[0]), float(
                msg.decode().split(',')[1]), float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]
        else:

            dados[str(client_address[0])] += [(float(msg.decode().split(',')[0]),
                                               float(msg.decode().split(',')[1]), float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]

        global new_data
        new_data = 1

        print('dados ---> ' + str(dados))

    conn.close()
    print(str(client_address) + ' - closed connection')
    _thread.exit()

#############################################################################


def connect():

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('', 9999)

    print('starting up on ' + str(server_address[0]) + ' port ' + str(server_address[1]))
    tcp.bind(server_address)

    tcp.listen(10)

    print('waiting for a connection... ')

    while True:

        (conn, client_address) = tcp.accept()
        print('connected with ' + str(client_address))

        _thread.start_new_thread(read, (conn, client_address))

    _thread.exit()

# ------------------------------------------------------------------------- #


_thread.start_new_thread(connect, ())


# ######################################################################### #
# ########################## Interface Grafica ############################ #
# ######################################################################### #

root = Tk()
root.title('1D Tracker')

while True:
    while new_data == 0:
        pass

    new_data = 0

    print('new data')

    for client_address in dados.keys():

        cliente = Label(root, text='Cliente ')
        cliente.grid(columnspan=4)

        label_1 = Label(root, text='Tensao [V]')
        label_2 = Label(root, text='Corrente [A]')
        label_3 = Label(root, text='Potencia [W]')
        label_4 = Label(root, text='Temperatura [C]')
        label_5 = Label(root, text='Orientacao [rad]')

        label_1.grid(column=0, row=1)
        label_2.grid(column=1, row=1)
        label_3.grid(column=2, row=1)
        label_4.grid(column=3, row=1)
        label_5.grid(column=4, row=1)

        i = 0

        while i < len(dados[client_address]):

            tensao_i = Label(root, text=str(dados[client_address][i][0]))
            corrente_i = Label(root, text=str(dados[client_address][i][1]))
            potencia_i = Label(root, text=str(
                dados[client_address][i][0] * dados[client_address][i][1]))
            temperatura_i = Label(root, text=str(dados[client_address][i][2]))
            orientacao_i = Label(root, text=str(dados[client_address][i][3]))

            tensao_i.grid(column=0, row=i + 2)
            corrente_i.grid(column=1, row=i + 2)
            potencia_i.grid(column=2, row=i + 2)
            temperatura_i.grid(column=3, row=i + 2)
            orientacao_i.grid(column=4, row=i + 2)

            i += 1

    root.update_idletasks()

    root.mainloop()
