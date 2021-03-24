from tkinter import *
from tkinter import ttk, messagebox
from config import Config
import mysql.connector


root = Tk()
root.title("Halaman Admin")
config = Config()

class DraggableWindow():
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonPress-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))

judul_kolom = ("ID", "Nama", "Username", "Password", "Role", "Departement")

class Admin:
    def __init__(self, parent):
        self.parent = parent
        #self.parent.protocol("WM_DELETE_WINDOWS")
        lebar = 750
        tinggi = 600
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        #self.parent.overrideredirect(1)
        self.komponen()


    def komponen(self):
        #atur frame
        top_level = Frame(self.parent, background='#cedfe0')
        top_level.pack(side=TOP, fill=X)
        Label(top_level, background='#cedfe0', font='{Segoe UI Black} 16 {}', text='Halaman Admin').pack(fill='x', side='top')
        input_frame = Frame(top_level, background='#cedfe0')
        input_frame.pack(side=TOP, fill=X)
        frame_button = Frame(top_level, background='#cedfe0')
        frame_button.pack(side=TOP, fill=X)
        self.frame_tabel = Frame(top_level)
        self.frame_tabel.pack(side=TOP, fill=Y, expand=YES, padx=10, pady=10)

        #input frame_label
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Kode').grid(column='0', padx='30', pady='10', row='0', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Nama').grid(column='0', padx='30', pady='10', row='1', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Username').grid(column='0', padx='30', pady='10', row='2', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Password').grid(column='0', padx='30', pady='10', row='3', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Role').grid(column='0', padx='30', pady='10', row='4', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Departement').grid(column='0', padx='30', pady='10', row='5', sticky='w')

        #input frame entry
        self.inputKode = Entry(input_frame, width='20', state='readonly')
        self.inputKode.grid(column='1', padx='20', row='0', sticky='w')
        self.inputNama = Entry(input_frame, width='50')
        self.inputNama.grid(column='1', padx='20', row='1', sticky='w')
        self.inputUsername = Entry(input_frame, width='30')
        self.inputUsername.grid(column='1', padx='20', row='2', sticky='w')
        self.inputPassword = Entry(input_frame, width='25')
        self.inputPassword.grid(column='1', padx='20', row='3', sticky='w')
        self.inputRole = Entry(input_frame, widt='25')
        self.inputRole.grid(column='1', padx='20', row='4', sticky='w')
        self.inputDepartement = Entry(input_frame, width='25')
        self.inputDepartement.grid(column='1', padx='20', row='5', sticky='w')

        #button frame
        Button(frame_button, command=self.onSave, font='{Arial} 10 {}', relief='groove', text='Simpan', width='8').grid(column='0', padx='15', pady='20', row='0', sticky='w')
        Button(frame_button, font='{Segoe UI Semibold} 10 {}', relief='groove', state='disabled', text='Update', width='8').grid(column='1', padx='15', pady='20', row='0', sticky='w')
        self.deleteButton = Button(frame_button, command=self.onDelete, font='{Arial} 10 {}', relief='groove', text='Hapus', width='8')
        self.deleteButton.grid(column='2', row='0', padx='15', pady='20', sticky='w' )

        #tabel
        self.trvTabel = ttk.Treeview(self.frame_tabel, columns=judul_kolom, show='headings')
        self.trvTabel.bind("<Double-1>")
        sbVer = Scrollbar(self.frame_tabel, orient='vertical', command=self.trvTabel.yview)
        sbVer.pack(side=RIGHT, fill=BOTH)
        self.trvTabel.pack(side=TOP, fill=BOTH, padx=10, pady=10)
        self.trvTabel.configure(yscrollcommand=sbVer.set)
        self.table()

    def onSave(self):
        entNama = self.inputNama.get()
        entUsername = self.inputUsername.get()
        entPassword = self.inputPassword.get()
        entRole = self.inputRole.get()
        entDepartement = self.inputDepartement.get()

        config.create(entNama, entUsername, entPassword, entRole, entDepartement)
        self.trvTabel.delete(*self.trvTabel.get_children())
        self.frame_tabel.after(0, self.table())

    def onDelete(self):
        selected_item = self.trvTabel.selection()[0]
        get_id = self.trvTabel.item(selected_item)['values'][0]
        config.delete(get_id)
        self.trvTabel.delete(*self.trvTabel.get_children())
        self.frame_tabel.after(0, self.table())

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)

        self.trvTabel.column("ID", width=90)
        self.trvTabel.column("Nama", width=150, anchor="w")
        self.trvTabel.column("Username", width=120)
        self.trvTabel.column("Password", width=90)
        self.trvTabel.column("Role", width=100)
        self.trvTabel.column("Departement", width=100)

        result = config.read()
        i=0
        for data in result:
            baris = "genap" if i%2 == 0 else "ganjil"
            self.trvTabel.insert('', 'end', values=data, tags=(baris, ))
            i+=1
        self.trvTabel.tag_configure("ganjil", background="#FFFFFF")
        self.trvTabel.tag_configure("genap", background="whitesmoke")








Admin(root)
root.mainloop()
