#-################### Servidor que recebe os dados ########################-#

import socket
import thread
from Tkinter import *

dados = {}

new_data = 0

#---------------------------------Threads-----------------------------------#

def read(conn, client_address):
    
    while True:
        
        msg = conn.recv(1024)
       
        if not msg: 
            print('no message received')
            break
        
        print ('received -->  ' +  msg)
        
        if msg == 'close': 
            break    
        
        global dados
        
        if str(client_address[0]) not in dados.keys():
            
            dados[str(client_address[0])] = [(float(msg.split(',')[0]) , float(msg.split(',')[1]))]
            
        else:
            
            dados[str(client_address[0])] += [(float(msg.split(',')[0]) , float(msg.split(',')[1]))]
        
        global new_data                
        new_data=1
        
        print ('dados ---> ' + str(dados))
    
        
    conn.close()    
    print (str(client_address) + ' - closed connection')
    thread.exit()
                 
#############################################################################

def connect():

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ('', 9999)
    
    print ('starting up on ' + str(server_address[0]) + ' port ' + str(server_address[1]))
    tcp.bind(server_address)
    
    tcp.listen(10)
    
    print ('waiting for a connection... ')
    
    while True:
    
        (conn, client_address) = tcp.accept()
        print ('connected with ' + str(client_address))
            
        thread.start_new_thread(read, (conn, client_address))
        
    thread.exit()
    
#---------------------------------------------------------------------------#

thread.start_new_thread(connect,())


#-######################## Interface Gráfica ##############################-#

root = Tk()
root.title('1D Tracker')

while True:
    while new_data == 0:
        pass
    
    new_data = 0
    
    print('new data')
    
    for client_address in dados.keys():
        
            cliente = Label(root, text='Cliente ')
            cliente.grid(columnspan=3)
            
            label_1 = Label(root, text='Tensao')
            label_2 = Label(root, text='Corrente')
            label_3 = Label(root, text='Potencia')
            
            label_1.grid(column=0, row=1)
            label_2.grid(column=1, row=1)
            label_3.grid(column=2, row=1)
        
        
            i = 0
            
            while i < len(dados[client_address]):
                
                tensao_i = Label(root, text=str(dados[client_address][i][0]))
                corrente_i = Label(root, text=str(dados[client_address][i][1]))
                potencia_i = Label(root, text=str(dados[client_address][i][0] * dados[client_address][i][1]))
                
                tensao_i.grid(column=0, row=i+2)
                corrente_i.grid(column=1, row=i+2)
                potencia_i.grid(column=2, row=i+2)
                
                i += 1
        
        
    root.update_idletasks()