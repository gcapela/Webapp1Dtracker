# ######################################################################### #
# ##################### Script que faz os graficos ######################## #
# ######################################################################### #

# TODO: meter dentro do scritpt do GUI ; arranjar uma maneira de meter o tempo a funcionar

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

tempo = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]

plt.title('Cliente XXXX')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):

    tensoes = []
    correntes = []
    potencias = []
    temperaturas = []
    orientacoes = []

    for tuplo in dados[str(client_address[0])]:
        (tensao, corrente, temperatura, orientacao) = tuplo.split(',')
        tensoes.append(tensao)
        correntes.append(corrente)
        potencias.append(tensao * corrente)
        temperaturas.append(temperatura)
        orientacoes.append(orientacao)

    ax1.clear()
    ax1.plot(tempo, tensoes, label='Tensao [V]')
    ax1.plot(tempo, correntes, label='Corrente [A]')
    ax1.plot(tempo, potencias, label='Potencia [W]')
    ax1.plot(tempo, temperaturas, label='Temperatura [C]')
    ax1.plot(tempo, orientacoes, label='Orientacao [rad]')


plt.xlabel('tempo [s]')
plt.ylabel('Valores')
plt.legend()

ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
