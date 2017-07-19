import matplotlib.pyplot as plt

tempo = [1, 2, 3, 4, 5, 6, 7, 8, 9]

tensao = [12, 11, 14.5, 13.2, 13.4, 12.8, 10, 12.1, 13.2]
corrente = [1.54, 1.6, 2, 1.8, 1.76, 1.8, 1.9, 1.51, 1.2]
potencia = [12 * 1.54, 11 * 1.6, 14.5 * 2, 13.2 * 1.8, 13.4 *
            1.76, 12.8 * 1.8, 10 * 1.9, 12.1 * 1.51, 13.2 * 1.2]
temperatura = [45, 43, 44, 40, 38, 37, 43, 45, 46]
orientacao = [0.38, 0.50, 0.63, 0.79, 0.96, 1.32, 1.64, 2.01, 2.87]


plt.title('Cliente XXXX')

plt.plot(tempo, tensao, label='Tensao')
plt.plot(tempo, corrente, label='Corrente')
plt.plot(tempo, potencia, label='Potencia')
plt.plot(tempo, temperatura, label='Temperatura')
plt.plot(tempo, orientacao, label='Orientacao')


plt.xlabel('tempo [s]')
plt.ylabel('Valores')

plt.legend()
plt.show()
