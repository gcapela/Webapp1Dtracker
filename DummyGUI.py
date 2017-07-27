import socket
import _thread
import tkinter as tk
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
matplotlib.use('TkAgg')

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

fig = Figure(figsize=(5, 5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):

    dados = open('LogFile.txt', 'r').read()
    dados_lista = dados.split('\n')
    del dados_lista[0]

    tensoes = []
    correntes = []
    potencias = []
    temperaturas = []
    orientacoes = []
    datas = []

    for linha in dados_lista:
        if len(linha) > 1:
            (tensao, corrente, temperatura, orientacao, data) = linha.split(',')
            tensoes.append(float(tensao))
            correntes.append(float(corrente))
            potencias.append(float(tensao) * float(corrente))
            temperaturas.append(float(temperatura))
            orientacoes.append(float(orientacao))
            dt = datetime.datetime.strptime(data, ' %Y-%m-%d %H:%M:%S')
            datas.append(dt)

    ax1.clear()
    ax1.plot(datas, tensoes, label='Tensao [V]')
    ax1.plot(datas, correntes, label='Corrente [A]')
    ax1.plot(datas, potencias, label='Potencia [W]')
    ax1.plot(datas, temperaturas, label='Temperatura [C]')
    ax1.plot(datas, orientacoes, label='Orientacao [rad]')

    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=45)
    plt.title('Cliente XXXX')
    plt.xlabel('Data')
    plt.ylabel('Valores')
    plt.legend()
    plt.tight_layout()


class Tracker1D(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, '1D Tracker')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = GUI(container, self)

        self.frames[GUI] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(GUI)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class GUI(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        cliente = tk.Label(self, text='Cliente XXXX')
        cliente.grid(columnspan=6)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # # label_1 = tk.Label(self, text='Data')
        # label_2 = tk.Label(self, text='Tensao [V]')
        # label_3 = tk.Label(self, text='Corrente [A]')
        # label_4 = tk.Label(self, text='Potencia [W]')
        # label_5 = tk.Label(self, text='Temperatura [C]')
        # label_6 = tk.Label(self, text='Orientacao [rad]')
        #
        # # label_1.grid(column=0, row=1)
        # label_2.grid(column=1, row=1)
        # label_3.grid(column=2, row=1)
        # label_4.grid(column=3, row=1)
        # label_5.grid(column=4, row=1)
        # label_6.grid(column=5, row=1)
        #
        # while True:
        #     global new_data
        #
        #     while new_data == 0:
        #         pass
        #
        #     for client_address in dados.keys():
        #
        #         i = 0
        #         j = 0
        #
        #         if(len(dados[client_address]) > 10):
        #             j = len(dados[client_address]) - 10
        #
        #         while i < len(dados[client_address]):
        #
        #             if i >= j:
        #
        #                 # data_i = Label(root, text=str(datetime.datetime.now()))
        #                 tensao_i = tk.Label(self, text=str(dados[client_address][i][0]))
        #                 corrente_i = tk.Label(self, text=str(dados[client_address][i][1]))
        #                 potencia_i = tk.Label(self, text=str(
        #                     dados[client_address][i][0] * dados[client_address][i][1]))
        #                 temperatura_i = tk.Label(self, text=str(dados[client_address][i][2]))
        #                 orientacao_i = tk.Label(self, text=str(dados[client_address][i][3]))
        #
        #                 # data_i.grid(column=0, row=i - j + 2)
        #                 tensao_i.grid(column=1, row=i - j + 2)
        #                 corrente_i.grid(column=2, row=i - j + 2)
        #                 potencia_i.grid(column=3, row=i - j + 2)
        #                 temperatura_i.grid(column=4, row=i - j + 2)
        #                 orientacao_i.grid(column=5, row=i - j + 2)
        #
        #             i += 1
        #
        #     new_data = 0


app = Tracker1D()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
