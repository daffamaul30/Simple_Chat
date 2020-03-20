import socket 
#from thread import *
from threading import Thread
import time
import numpy as np
import datetime

#membuat socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 


BUFFSIZE = 4096000 #set BUFFSIZE to 4096000
IP_address = ''
Port = 10002 #set Port
server_address = (IP_address,Port)
print("Waiting for connection on Port %s" % (Port))  
server.bind((server_address)) #bind

server.listen(100) #listen
  
username = {} #deklarasi dictionary username
list_of_clients = [] #deklarasi list list_of_clients
Pesan = [] #deklarasi list Pesan
  
#membuat function clientthread
def clientthread(conn, addr):  
    name = conn.recv(20) #menerima username dari client
    username[addr[0]] = name #memasukkan ip dan username ke dalam dictionary username
    
    while True: 
        try:
            pesan = conn.recv(BUFFSIZE).decode("utf8") #menerima pesan
            if pesan.startswith('teks'): #kondisi ketika pesan diawali dengan kata "teks"
                rcv_text(conn, addr, pesan) #menjalankan function rcv_text
            elif pesan.startswith('histori'): #kondisi ketika pesan diawali dengan kata "histori"
                rcv_history(conn, addr) #menjalankan function rcv_history
            elif pesan.startswith('gambar'): #kondisi ketika pesan diawali dengan kata "gambar"
                rcv_image(conn, addr, pesan) #menjalankan function rcv_image
        except:
            continue

#membuat function rcv_history
def rcv_history(conn, addr):
    #mengirimkan kode histori ke client
    kodek = 'histori'
    conn.send(kodek)
    print("HISTORY : ")
    #mengirimkan histori ke client
    for i in range(0,len(Pesan)):
        print(Pesan[i])
        conn.send(Pesan[i]+"#")

#membuat function rcv_text
def rcv_text(conn, addr, pesan):
    if pesan: #kondisi jika pesan tidak 0
        tmp = pesan.split('#')
        localtime = time.ctime() #mengambil nilai waktu saat ini
        psn = localtime + " " + " <" + username[addr[0]] + "> " + tmp[1] #menggabungkan localtime,username dan pesan
        print(psn)
        Pesan.append(psn) #menambahkan psn ke list Pesan

        tm = datetime.datetime.now() #mengambil nilai waktu dengan format yang berbeda dengan sebelumnya
        waktu = "%s:%s" %(tm.hour,tm.minute) #mengambil nilai jam dan menit

        message_to_send = "teks" + "#" + "<" + username[addr[0]] + "> " + tmp[1] + "   " + waktu #menggabungkan kode#,username, pesan dan waktu
        broadcast(message_to_send, conn) #kirim message_to_send ke client lain dengan function broadcast
    else: 
        remove(conn) 

def rcv_image(conn, addr, pesan):
    if pesan:
        data = conn.recv(BUFFSIZE) #menerima data dari client

        tm = datetime.datetime.now() #mengambil nilai waktu dengan format yang berbeda dengan sebelumnya
        waktu = "%s:%s" %(tm.hour,tm.minute) #mengambil nilai jam dan menit
        broadcast(pesan, conn)  #kirim kembali pesan yang dikirim client, ke client lain dengan function broadcast
        #conn.send(pesan) #jika mau test 1 client saja
        message_to_send = "<" + username[addr[0]] + "> " + "Sent an image" + "   " + waktu  #menggabungkan kode#,username, pesan dan waktu
        broadcast(message_to_send, conn) #kirim message_to_send ke client lain dengan function broadcast
        #conn.send(message_to_send) #jika mau test 1 client saja

        localtime = time.ctime() #mengambil nilai waktu saat ini
        psn = localtime + " " + " <" + username[addr[0]] + "> " + "Sent an imageee" #menggabungkan localtime,username dan pesan
        print(psn)
        Pesan.append(psn) #menambahkan psn ke list Pesan

        broadcast(data, conn) #kirim data yang dikirimkan client, ke client lain dengan function broadcast
        #conn.send(data) #jika mau test 1 client saja
    else:
        remove(conn)

#membuat function broadcast
def broadcast(message, connection): 
    for clients in list_of_clients: #loop semua isi list_of_clients sebagai clients
        if clients!=connection: #kondisi jika clients != connection (clients bukan client pengirim)
            try: 
                clients.send(message) #mengirim pesan ke clients
            except: 
                clients.close() 
                remove(clients) 

#membuat function remove
def remove(connection): 
    if connection in list_of_clients: #kondisi jika connection ada di dalam list_of_clients
        list_of_clients.remove(connection) #connection di remove


while True: 
    conn, addr = server.accept() #accept connection dari client
    list_of_clients.append(conn) #memasukkan conn ke list_of_clients
    print (addr[0] + " connected")
    
    receive_thread = Thread(target=clientthread(conn,addr)) #menggunakan thread untuk menjalankan function recieve pada class app
    receive_thread.start()
    #start_new_thread(clientthread,(conn,addr)) #menjalankan function clientthread dengan thread  
conn.close() 
server.close() 