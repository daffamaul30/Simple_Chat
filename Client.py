from tkinter import *
from tkinter import filedialog
from threading import Thread
import socket
from socket import AF_INET, SOCK_STREAM
import datetime
import random
from random import randint
import io

#membuat Window Connect dengan class connect() untuk connect ke server dan menginputkan username
class connect(Frame):

    #pembentukan Frame
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.tampil = parent
        self.tampil.configure(bg='#fcba03') #mengubah warna background
        self.tampil.iconbitmap(r'C:\Users\ASUS\Downloads\Simple_Chat\i.ico') #mengubah icon window (atur sesuai direktori penyimpanan file .ico)
        self.tampil.title('Connect') #mengubah title window
        self.tampil.geometry("200x100+660+350") #mengubah size dan posisi window
        self.tampil.resizable(0, 0) #agar size window tidak dapat dirubah

        #membuat label
        self.l1 = Label(text="IP SERVER : ", background="#fcba03", font="Helvetica 7").grid(row=0)
        self.l2 = Label(text="IP PORT   : ", background="#fcba03", font="Helvetica 7").grid(row=1)
        self.l2 = Label(text="USERNAME  : ", background="#fcba03", font="Helvetica 7").grid(row=2)

        #membuat entry
        self.e1 = Entry(font="Helvetica 8")
        self.e2 = Entry(font="Helvetica 8")
        self.e3 = Entry(font="Helvetica 8")

        #mengatur grid dari entry
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        #membuat button Ok
        self.buton = Button(text='Ok', command=self.konek, width='10')
        self.buton['border'] = '1'
        self.buton.place(x=110,y=70)

    #membuat function konek untuk dipanggil ketika button Ok ditekan
    def konek(self):
        #mengambil nilai inputan dari entry sebelumnya
        self.ip = self.e1.get()
        self.port = self.e2.get()
        self.user = self.e3.get()
        self.tampil.destroy() #destroy window untuk menutup
        
#membuat Window App(utama) dengan class App() untuk memulai chat
class App(Frame):
    #pembentukan Frame
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#fcba03')
        self.tampilan = parent
        self.tampilan.iconbitmap(r'C:\Users\ASUS\Downloads\Simple_Chat\i.ico')
        self.tampilan.title("Chatto")
        self.pack(fill=BOTH, expand=1)
        self.tampilan.geometry("400x500+560+150")
        self.tampilan.resizable(0, 0)
        
        #membuat button History
        self.btn = Button(self, text='History', width='22', height='1', font="Helvetica 10", command=self.histori)
        self.btn['border'] = '1'
        self.btn.place(x=11, y=10)

        #membuat button Clear History
        self.btn2 = Button(self, text='Clear History', width='22', height='1', font="Helvetica 10", command=self.clear_histori)
        self.btn2['border'] = '1'
        self.btn2.place(x=207, y=10)

        #membuat space untuk history
        self.history_frame = Frame(self)#membuat frame
        self.scrollbar1 = Scrollbar(self.history_frame)#membuat scrollbar di dalam frame
        self.msg_list1 = Listbox(self.history_frame, height=8, width=60, yscrollcommand=self.scrollbar1.set, font="Helvetica 8")#membuat listbox di dalam frame untuk menampilkan history
        self.scrollbar1.pack(side=RIGHT, fill=Y)#memposisikan scrollbar di kanan frame
        self.msg_list1.pack(side=LEFT, fill=BOTH)#memposisikan listbox di kiri frame
        self.msg_list1.pack()
        self.history_frame.place(x=10, y=45)#mengatur posisi frame
        
        #membuat space untuk menampilkan pesan
        self.messages_frame = Frame(self)#membuat frame
        self.scrollbar = Scrollbar(self.messages_frame)#membuat scrollbar di dalam frame
        self.msg_list = Listbox(self.messages_frame, height=16, width=60, yscrollcommand=self.scrollbar.set, font="Helvetica 8")#membuat listbox di dalam frame untuk menampilkan pesan
        self.scrollbar.pack(side=RIGHT, fill=Y)#memposisikan scrollbar di kanan frame
        self.msg_list.pack(side=LEFT, fill=BOTH)#memposisikan listbox di kiri frame
        self.msg_list.pack()
        self.messages_frame.place(x=10, y=180)#mengatur posisi frame

        #membuat button send untuk mengirim
        self.send_button = Button(self, text="Send", width='14', height='1', font="Helvetica 8", bd=5, command=self.send)
        self.send_button['border'] = '1'
        self.send_button.place(x=299, y=440)

        #membuat Text sebagai pengganti entry untuk mengetikkan pesan
        self.pesan = Text(self, width=46, height='3', font="Helvetica 8")
        self.pesan['border'] = '1'
        self.pesan.place(x=10, y=440)

        #membuat button choose image untuk memilih gambar yang akan dikirim
        self.chose = Button(self, text='Choose Image', width='14', height='1', font="Helvetica 8", bd=5, command=self.chooseFile)
        self.chose['border'] = '1'
        self.chose.place(x=299, y=465)

        self.BUFFSIZE = 4096000 #mengatur ukuran BUFFSIZE dengan asign ke variabel BUFFSIZE

    #membuat function histori
    def histori(self):
        #mengirimkan code "histori" ke server
        code = "histori"
        server.send(bytes(code,"utf8"))

    #membuat function clear_histori
    def clear_histori(self):
        self.msg_list1.delete(0,END)

    #membuat function chooseFile
    def chooseFile(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a Photo", filetype =(("png files","*.png*"),("jpeg files","*.jpg")))#membuat fileDialog agar dapat memilih gambar dari direktori
        myfile = open(self.filename,'rb')#membuka file gambar dan dimasukkan ke variabel myfile
        byte = myfile.read()#membaca myfile dan di asign ke variabel byte
        #mengirimkan kode "gambar#" ke server
        code = "gambar#"
        server.send(bytes(code,"utf8"))
        server.send(byte) #mengirim variabel byte ke server
        localtime = datetime.datetime.now() #mengambil nilai waktu saat ini
        waktu =  "%s:%s" %(localtime.hour,localtime.minute) #mengambil niali jam dan menit
        self.msg_list.insert(END," <You> : " + "Sent a an image" + "   " + waktu) #insert ke listbox msg_list untuk menampilkan pesan
        myfile.close() #menutup myfile

    #membuat function send
    def send(self):
        #hanya dapat mengirimkan pesan jika panjang dari pesan yang dimasukkan lebih dari 1 (karena defaultnya udah ada 1 char)
        if(len(self.pesan.get('1.0', END)) > 1 ):
            code = "teks#"
            self.msg = self.pesan.get('1.0', END) #mengambil inputan pesan dan di asign ke variabel msg
            self.pesan.delete('1.0',END) #menghapus inputan pesan agar entry untuk mengetikkan pesan kembali kosong
            server.send(bytes(code+self.msg,"utf8")) #mengirim code+msg ke server dengan encode utf8
            localtime = datetime.datetime.now() #mengambil nilai waktu saat ini
            waktu =  "%s:%s" %(localtime.hour,localtime.minute) #mengambil niali jam dan menit
            self.msg_list.insert(END," <You> : " + self.msg + "   " + waktu) #insert ke listbox msg_list untuk menampilkan pesan

    #membuat function receive
    def receive(self):
        count = 1 #set nilai count
        while True: #terus menjalankan ketika True
            code = server.recv(4096).decode("utf8") #menerima pesan yang dikirimkan server
            kode = code.split('#') #split pesan dengan # untuk memisahkan kode dan pesan

            if kode[0]=="teks": #kondisi ketika kode = teks
                self.msg_list.insert(END, kode[1]) #memasukkan pesan ke msg_list
            elif kode[0]=="gambar": #kondisi ketika kode = gambar
                basename = 'image%s.png' #set basename
                try:
                    rec = server.recv(28) #menerima pesan "sent an image"
                    self.msg_list.insert(END, rec) #memasukkan pesan ke msg_list
                    data = server.recv(self.BUFFSIZE) #menerima pesan dari server
                    myfile = open(basename % count, 'wb') #open file dengan nama sesuai basename dan count
                    myfile.write(data) #menulis data pada myfile(file yang sudah diopen tadi)
                    myfile.close() #menutup myfile

                    #menampilkan popup gambar
                    top = Toplevel()
                    diagrams = PhotoImage(file='image' +str(count)+ '.png')
                    logolbl= Label(top, image = diagrams)
                    logolbl.grid()
                    top.mainloop()

                    count+=1 #count bertambah
                except:
                    continue
            elif code=="histori": #ketika kode = histori
                hstr = str(server.recv(self.BUFFSIZE)) #menerima pesan dari server
                x = hstr.split("#") #split dengan #
                x[0] = x[0][2:] #cut histori pertama dari 2-habis

                #insert semua histori ke msg_list1 untuk menampilkan histori
                for i in range(len(x)):
                    x[i] = x[i][0:len(x[i])-2]
                    self.msg_list1.insert(END, x[i])

hubung = Tk()
hubungkan = connect(hubung)

hubung.mainloop()

IP = hubungkan.ip #ambil nilai variabel ip pada class connect
Port = hubungkan.port #ambil nilai variabel port pada class connect
user = hubungkan.user #ambil nilai variabel user pada class connect

root = Tk()
app = App(root) 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #membuat socket TCP

Server_address = (IP, int(Port))
server.connect(Server_address) #connect ke server

server.send(bytes(user,"utf8")) #mengirimkan username ke server

#menggunakan thread untuk menjalankan function recieve pada class app
receive_thread = Thread(target=app.receive) #menggunakan thread untuk menjalankan function recieve pada class app
receive_thread.start()

root.mainloop()
server.close() #close server