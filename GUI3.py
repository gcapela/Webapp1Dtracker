# Versão 3.0 - 20/07/2017

# ######################################################################### #
# ############################## Servidor ################################# #
# ######################################################################### #

import socket
import _thread
# import threading
# import time
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
        global new_data

        if str(client_address[0]) not in dados.keys():

            dados[str(client_address[0])] = [(float(msg.decode().split(',')[0]), float(msg.decode().split(',')[1]),
                                              float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]
            saveFile = open('LogFile.txt', 'w')
            saveFile.write(" V ,   A  , C , rad\n")
            saveFile.write(msg.decode() + '\n')
            saveFile.close()
            new_data +=1

        else:

            dados[str(client_address[0])] += [(float(msg.decode().split(',')[0]), float(msg.decode().split(',')[1]),
                                               float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]
            appendFile = open('LogFile.txt', 'a')
            appendFile.write(msg.decode() + '\n')
            appendFile.close()
            new_data +=1


        print('dados ---> ' + str(dados))

        print(len(dados))

        print('NEW_DATA:')

        print(new_data)

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

def GUIcheck():

    root = Tk()
    root.title('1D Tracker')

    # for client_address in dados.keys():

    cliente = Label(root, text='Cliente ')
    cliente.grid(columnspan=10)

    label_1 = Label(root, text='Tensao [V]')
    label_2 = Label(root, text='Corrente [A]')
    label_3 = Label(root, text='Potencia [W]')
    label_4 = Label(root, text='Temperatura [C]')
    label_5 = Label(root, text='Orientacao [rad]')

    label_1.grid(column=0, row=1)
    label_2.grid(column=2, row=1)
    label_3.grid(column=4, row=1)
    label_4.grid(column=6, row=1)
    label_5.grid(column=8, row=1)

    root.update_idletasks()
    root.update()

    while True:
        global new_data

        while new_data == 0:
            pass

        print('new data')

        for client_address in dados.keys():

            i = 0
            j = 0
            k = 0

            if(k==0)

            print('dados_2 ---> ' + str(dados))

            print('NEM_DATA_2')

            while i >= j and i < len(dados[client_address]):

                tensao_i = Label(root, text=str(dados[client_address][i][0]))
                corrente_i = Label(root, text=str(dados[client_address][i][1]))
                potencia_i = Label(root, text=str(
                    dados[client_address][i][0] * dados[client_address][i][1]))
                temperatura_i = Label(root, text=str(dados[client_address][i][2]))
                orientacao_i = Label(root, text=str(dados[client_address][i][3]))

                tensao_i.grid(column=0, row=i-j + 2)
                corrente_i.grid(column=2, row=i-j + 2)
                potencia_i.grid(column=4, row=i-j + 2)
                temperatura_i.grid(column=6, row=i-j + 2)
                orientacao_i.grid(column=8, row=i-j + 2)

                i += 1

                if i>=10:
                    j += 1
                    print(j)

        new_data = 0

        root.update_idletasks()
        root.update()

_thread.start_new_thread(GUIcheck, ())

while True:
    pass
