from tkinter import *
from tkinter import filedialog
from threading import Thread
import socket
from socket import AF_INET, SOCK_STREAM
import datetime
import random
from random import randint
import io

class connect(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.tampil = parent
        self.tampil.configure(bg='#fcba03')
        self.tampil.title('Connect')
        self.tampil.geometry("200x100+660+350")
        self.tampil.resizable(0, 0)

        self.l1 = Label(text="IP SERVER : ", background="#fcba03", font="Helvetica 7").grid(row=0)
        self.l2 = Label(text="IP PORT   : ", background="#fcba03", font="Helvetica 7").grid(row=1)
        self.l2 = Label(text="USERNAME  : ", background="#fcba03", font="Helvetica 7").grid(row=2)

        self.e1 = Entry(font="Helvetica 8")
        self.e2 = Entry(font="Helvetica 8")
        self.e3 = Entry(font="Helvetica 8")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        self.buton = Button(text='Ok', command=self.konek, width='10')
        self.buton['border'] = '1'
        self.buton.place(x=110,y=70)

    def konek(self):
        self.ip = self.e1.get()
        self.port = self.e2.get()
        self.user = self.e3.get()
        self.tampil.destroy()
        

class App(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#fcba03')
        self.tampilan = parent
        self.tampilan.iconbitmap(r'C:\Users\ASUS\Downloads\Simple_Chat\i.ico')
        self.tampilan.title("Chatto")
        self.pack(fill=BOTH, expand=1)
        self.tampilan.geometry("400x500+560+150")
        self.tampilan.resizable(0, 0)
        
        self.btn = Button(self, text='History', width='22', height='1', font="Helvetica 10", command=self.histori)
        self.btn['border'] = '1'
        self.btn.place(x=11, y=10)

        self.btn2 = Button(self, text='Clear History', width='22', height='1', font="Helvetica 10", command=self.clear_histori)
        self.btn2['border'] = '1'
        self.btn2.place(x=207, y=10)

        self.history_frame = Frame(self)
        self.scrollbar1 = Scrollbar(self.history_frame)
        self.msg_list1 = Listbox(self.history_frame, height=8, width=60, yscrollcommand=self.scrollbar1.set, font="Helvetica 8")
        self.scrollbar1.pack(side=RIGHT, fill=Y)
        self.msg_list1.pack(side=LEFT, fill=BOTH)
        self.msg_list1.pack()
        self.history_frame.place(x=10, y=45)
        
        self.messages_frame = Frame(self)
        self.scrollbar = Scrollbar(self.messages_frame)
        self.msg_list = Listbox(self.messages_frame, height=16, width=60, yscrollcommand=self.scrollbar.set, font="Helvetica 8")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH)
        self.msg_list.pack()
        self.messages_frame.place(x=10, y=180)

        self.send_button = Button(self, text="Send", width='14', height='1', font="Helvetica 8", bd=5, command=self.send)
        self.send_button['border'] = '1'
        self.send_button.place(x=299, y=440)

        self.pesan = Text(self, width=46, height='3', font="Helvetica 8")
        self.pesan['border'] = '1'
        self.pesan.place(x=10, y=440)

        self.chose = Button(self, text='Choose Image', width='14', height='1', font="Helvetica 8", bd=5, command=self.chooseFile)
        self.chose['border'] = '1'
        self.chose.place(x=299, y=465)

        self.BUFFSIZE = 4096000

    def histori(self):
        code = "histori"
        server.send(bytes(code,"utf8"))

    def clear_histori(self):
        self.msg_list1.delete(0,END)

    def chooseFile(self):
        
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a Photo", filetype =(("png files","*.png*"),("jpeg files","*.jpg")))
        myfile = open(self.filename,'rb')
        byte = myfile.read()
        #print(byte)
        code = "gambar#"
        server.send(bytes(code,"utf8"))
        #codebyte = bytes(code+str(byte),"utf8")
        server.send(byte)
        localtime = datetime.datetime.now()
        waktu =  "%s:%s" %(localtime.hour,localtime.minute)
        self.msg_list.insert(END," <You> : " + "Sent a an image" + "   " + waktu)
        myfile.close()

    def send(self):  # event is passed by binders.
        """Handles sending of messages."""
        if(len(self.pesan.get('1.0', END)) > 1 ):
            code = "teks#"
            #server.send(bytes(code,"utf8"))
            self.msg = self.pesan.get('1.0', END)
            self.pesan.delete('1.0',END)  # Clears input field.
            server.send(bytes(code+self.msg,"utf8"))
            localtime = datetime.datetime.now()
            waktu =  "%s:%s" %(localtime.hour,localtime.minute)
            self.msg_list.insert(END," <You> : " + self.msg + "   " + waktu)

    def receive(self):
        count = 1
        while True:
            #print("a")
            code = server.recv(4096).decode("utf8")
            #print("b",code)
            kode = code.split('#')
            #print(kode[0])

            if kode[0]=="teks":
                #message = server.recv(self.BUFFSIZE).decode("utf8")
                self.msg_list.insert(END, kode[1])
            elif kode[0]=="gambar":
                basename = 'image%s.png'
                try:
                    #print("mulai")
                    rec = server.recv(28)
                    #print("mulai1",rec)
                    self.msg_list.insert(END, rec)
                    #print("mulai2")
                    data = server.recv(self.BUFFSIZE)
                    gata = data
                    #print(data)           
                    #print(1)
                    myfile = open(basename % count, 'wb')
                    #print(2)
                    myfile.write(gata)
                    #print(3)
                    myfile.close()
                    #print(4)

                    top = Toplevel()
                    diagrams = PhotoImage(file='image' +str(count)+ '.png')
                    logolbl= Label(top, image = diagrams)
                    logolbl.grid()
                    count+=1
                    top.mainloop()
                except:
                    continue
            elif code=="histori":
                hstr = str(server.recv(self.BUFFSIZE))
                x = hstr.split("#")
                x[0] = x[0][2:]
                for i in range(len(x)):
                    x[i] = x[i][0:len(x[i])-2]
                    self.msg_list1.insert(END, x[i])

hubung = Tk()
hubungkan = connect(hubung)

hubung.mainloop()

IP = hubungkan.ip
Port = hubungkan.port
user = hubungkan.user
#print(user)

root = Tk()
app = App(root)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Server_address = (IP, int(Port))
server.connect(Server_address)

server.send(bytes(user,"utf8"))

receive_thread = Thread(target=app.receive)
receive_thread.start()

root.mainloop()
server.close() 