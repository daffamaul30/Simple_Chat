import socket 
import pickle
import select 
import sys 
from thread import *
from threading import Thread
import time
import cv2
import numpy as np
import datetime
import io

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 


BUFFSIZE = 4096000
IP_address = ''
Port = 10002
server_address = (IP_address,Port)
print("Waiting for connection on %s Port" % (Port))  
server.bind((server_address)) 

server.listen(100) 
  
list_of_clients = []
Pesan = []
  
def clientthread(conn, addr):      
    while True: 
        try:
            pesan = conn.recv(BUFFSIZE).decode("utf8")
            if pesan.startswith('teks'):
                rcv_text(conn, addr, pesan)
            elif pesan.startswith('histori'):
                rcv_history(conn, addr)
            elif pesan.startswith('gambar'):
                rcv_image(conn, addr, pesan)
        except:
            continue

def rcv_history(conn, addr):
    kodek = 'histori'
    conn.send(kodek)
    for i in range(0,len(Pesan)):
        print(Pesan[i])
        conn.send(Pesan[i]+"#")

def rcv_text(conn, addr, pesan):
    if pesan:
        tmp = pesan.split('#')
        localtime = time.ctime()
        psn = localtime + " " + " <" + addr[0] + "> " + tmp[1]
        print(psn)
        Pesan.append(psn)

        tm = datetime.datetime.now()
        waktu = "%s:%s" %(tm.hour,tm.minute)

        message_to_send = "teks" + "#" + "<" + addr[0] + "> " + tmp[1] + "   " + waktu
        broadcast(message_to_send, conn) 
    else: 
        remove(conn) 

def rcv_image(conn, addr, pesan):
    if pesan:
        data = conn.recv(BUFFSIZE)

        localtime = time.ctime()
        psn = localtime + " " + " <" + addr[0] + "> " + "Sent an imageee"
        print(psn)
        Pesan.append(psn)
        tm = datetime.datetime.now()

        waktu = "%s:%s" %(tm.hour,tm.minute)
        broadcast(pesan, conn)
        #conn.send(pesan)
        message_to_send = "<" + addr[0] + "> " + "Sent an image" + "   " + waktu
        broadcast(message_to_send, conn)
        #conn.send(message_to_send)
        broadcast(data, conn)
        #conn.send(data)
    else:
        remove(conn)

def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                remove(clients) 
  
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 


while True: 
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    
    start_new_thread(clientthread,(conn,addr))   
conn.close() 
server.close() 
 
#python Server.py 192.168.1.17 10002