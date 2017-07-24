# Versao 3.1 - 24/07/2017

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
        global new_data

        if str(client_address[0]) not in dados.keys():

            dados[str(client_address[0])] = [(float(msg.decode().split(',')[0]), float(msg.decode().split(',')[1]),
                                              float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]
            saveFile = open('LogFile.txt', 'w')
            saveFile.write(" V ,   A  , C , rad \n")
            saveFile.write(msg.decode() + '\n')
            saveFile.close()

        else:

            dados[str(client_address[0])] += [(float(msg.decode().split(',')[0]), float(msg.decode().split(',')[1]),
                                               float(msg.decode().split(',')[2]), float(msg.decode().split(',')[3]))]
            appendFile = open('LogFile.txt', 'a')
            appendFile.write(msg.decode() + '\n')
            appendFile.close()

        new_data += 1
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

def GUIcheck():

    root = Tk()
    root.title('1D Tracker')

    # for client_address in dados.keys():

    cliente = Label(root, text='Cliente ')
    cliente.grid(columnspan=5)

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

    root.update_idletasks()
    root.update()

    while True:
        global new_data

        while new_data == 0:
            pass

        for client_address in dados.keys():

            i = 0
            j = 0

            if(len(dados[client_address]) > 10):
                j = len(dados[client_address]) - 10

            while i < len(dados[client_address]):

                if i >= j:

                    tensao_i = Label(root, text=str(dados[client_address][i][0]))
                    corrente_i = Label(root, text=str(dados[client_address][i][1]))
                    potencia_i = Label(root, text=str(
                        dados[client_address][i][0] * dados[client_address][i][1]))
                    temperatura_i = Label(root, text=str(dados[client_address][i][2]))
                    orientacao_i = Label(root, text=str(dados[client_address][i][3]))

                    tensao_i.grid(column=0, row=i - j + 2)
                    corrente_i.grid(column=1, row=i - j + 2)
                    potencia_i.grid(column=2, row=i - j + 2)
                    temperatura_i.grid(column=3, row=i - j + 2)
                    orientacao_i.grid(column=4, row=i - j + 2)

                i += 1

        new_data = 0

        root.update_idletasks()
        root.update()


_thread.start_new_thread(GUIcheck, ())

while True:
    pass
