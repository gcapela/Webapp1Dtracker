# ######################################################################### #
# ##################### Script que faz os graficos ######################## #
# ######################################################################### #

# TODO: meter dentro de uma thread no scritpt do GUI

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import datetime

fig = plt.figure()
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


ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
