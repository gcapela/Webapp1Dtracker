# Versao 4.0 - 27/07/2017

# ######################################################################### #
# ############################## Servidor ################################# #
# ######################################################################### #

import socket
import _thread
from tkinter import *
import datetime

dados = {}

new_data = 0

# --------------------------------Threads---------------------------------- #


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

        mds = msg.decode().split(',')
        data = datetime.datetime.now().replace(microsecond=0)

        if str(client_address[0]) not in dados.keys():

            dados[str(client_address[0])] = [(float(mds[0]), float(mds[1]),
                                              float(mds[2]), float(mds[3]))]
            saveFile = open('LogFile.txt', 'w')
            saveFile.write(" V ,   A  ,  C ,  rad ,  data \n")
            saveFile.write(msg.decode() + ' , ' + str(data) + '\n')
            saveFile.close()

        else:

            dados[str(client_address[0])] += [(float(mds[0]), float(mds[1]),
                                               float(mds[2]), float(mds[3]))]
            appendFile = open('LogFile.txt', 'a')
            appendFile.write(msg.decode() + ' , ' + str(data) + '\n')
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
# ################################ Tabela ################################# #
# ######################################################################### #

def Tabela():

    root = Tk()
    root.title('1D Tracker')

    # TODO: acrescentar possibilidade para varios clientes - for client_address in dados.keys():
    # TODO: acrescentar data dos valores a tabela

    cliente = Label(root, text='Cliente XXXX')
    cliente.grid(columnspan=6)

    # label_1 = Label(root, text='Data')
    label_2 = Label(root, text='Tensao [V]')
    label_3 = Label(root, text='Corrente [A]')
    label_4 = Label(root, text='Potencia [W]')
    label_5 = Label(root, text='Temperatura [C]')
    label_6 = Label(root, text='Orientacao [rad]')

    # label_1.grid(column=0, row=1)
    label_2.grid(column=1, row=1)
    label_3.grid(column=2, row=1)
    label_4.grid(column=3, row=1)
    label_5.grid(column=4, row=1)
    label_6.grid(column=5, row=1)

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

                    # data_i = Label(root, text=str(datetime.datetime.now()))
                    tensao_i = Label(root, text=str(dados[client_address][i][0]))
                    corrente_i = Label(root, text=str(dados[client_address][i][1]))
                    potencia_i = Label(root, text=str(
                        dados[client_address][i][0] * dados[client_address][i][1]))
                    temperatura_i = Label(root, text=str(dados[client_address][i][2]))
                    orientacao_i = Label(root, text=str(dados[client_address][i][3]))

                    # data_i.grid(column=0, row=i - j + 2)
                    tensao_i.grid(column=1, row=i - j + 2)
                    corrente_i.grid(column=2, row=i - j + 2)
                    potencia_i.grid(column=3, row=i - j + 2)
                    temperatura_i.grid(column=4, row=i - j + 2)
                    orientacao_i.grid(column=5, row=i - j + 2)

                i += 1

        new_data = 0

        root.update_idletasks()
        root.update()


_thread.start_new_thread(Tabela, ())

while True:
    pass
