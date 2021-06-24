from tkinter import *
from tkinter import ttk, messagebox
from config import Config
import os
import mysql.connector

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")
# config = Config()
judul_kolom = ("ID", "Nama", "Username", "Password", "Bagian")

class Admin(Config):
    def __init__(self, parent):
        super(Admin, self).__init__()
        self.parent = parent
        lebar = 750
        tinggi = 740
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        #self.parent.overrideredirect(1)
        self.komponen()


    def komponen(self):
        #atur frame
        top_level = Frame(self.parent, background='#cedfe0')
        top_level.pack(side=TOP, fill=X)
        Label(top_level, background='#808080', font='{Segoe UI Semibold} 14 {}', text='Halaman Kelola Pengguna', padx='10', pady='20').pack(fill='x', side='top')
        input_frame = Frame(top_level, background='#cedfe0')
        input_frame.pack(side=TOP, fill=X)
        self.frame_button = Frame(top_level, background='#cedfe0')
        self.frame_button.pack(side=TOP, fill=X)
        self.frame_tabel = Frame(top_level)
        self.frame_tabel.pack(side=TOP, fill='both', expand=YES, padx=10, pady=10)
        self.frame_menu = Frame(top_level, background='#cedfe0')
        self.frame_menu.pack(side=TOP, fill='y', expand=YES)

        #input frame_label
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Kode').grid(column='0', padx='30', pady='10', row='0', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Nama').grid(column='0', padx='30', pady='10', row='1', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Username').grid(column='0', padx='30', pady='10', row='2', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Password').grid(column='0', padx='30', pady='10', row='3', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Konfirmasi Password').grid(column='0', padx='30', pady='10', row='4', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Pengelola Bagian').grid(column='0', padx='30', pady='10', row='5', sticky='w')

        #input frame entry
        readonlytext = StringVar()
        readonlytext.set('Dikembangkan Otomatis')
        self.inputKode = Entry(input_frame, width='25', state='normal', textvariable=readonlytext)
        self.inputKode.grid(column='1', padx='20', row='0', sticky='w')
        self.inputKode.config(state='disabled')
        self.inputNama = Entry(input_frame, width='50')
        self.inputNama.grid(column='1', padx='20', row='1', sticky='w')
        self.inputUsername = Entry(input_frame, width='30')
        self.inputUsername.grid(column='1', padx='20', row='2', sticky='w')
        self.inputPassword = Entry(input_frame, width='25', show='•')
        self.inputPassword.grid(column='1', padx='20', row='3', sticky='w')
        self.inputKonfirmasi = Entry(input_frame, widt='25', show='•')
        self.inputKonfirmasi.grid(column='1', padx='20', row='4', sticky='w')
        self.inputBagian = Entry(input_frame, width='25')
        self.inputBagian.grid(column='1', padx='20', row='5', sticky='w')

        #button frame
        self.saveButton = Button(self.frame_button, command=self.onSave, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Simpan', width='8')
        self.saveButton.grid(column='0', padx='30', pady='20', row='0', sticky='w')
        self.updateButton = Button(self.frame_button, font='{Segoe UI Semibold} 10 {}', relief='groove', state='disabled', text='Update', width='8', command=self.onUpdate)
        self.updateButton.grid(column='1', padx='30', pady='20', row='0', sticky='w')
        self.deleteButton = Button(self.frame_button, command=self.onDelete, state='disabled', font='{Segoe UI Semibold} 10 {}', relief='groove', text='Hapus', width='8')
        self.deleteButton.grid(column='2', row='0', padx='30', pady='20', sticky='w')
        self.clearButton = Button(self.frame_button, font='{Segoe UI Semibold} 10 {}', command=self.onClear, relief='groove', text='Clear', width='8')
        self.clearButton.grid(column='3', row='0', sticky='w', padx='30')
        self.backButton = Button(self.frame_menu, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Kembali', width='8', command=self.onKembali)
        self.backButton.grid(column='0', row='0', padx='30', pady='10', sticky='w')

        #tabel
        self.trvTabel = ttk.Treeview(self.frame_tabel, columns=judul_kolom, show='headings')
        self.trvTabel.bind("<Double-1>", self.onDoubleClick)
        sbVer = Scrollbar(self.frame_tabel, orient='vertical', command=self.trvTabel.yview)
        sbVer.pack(side=RIGHT, fill=BOTH)
        self.trvTabel.pack(side=TOP, fill=BOTH, padx=10, pady=10)
        self.trvTabel.configure(yscrollcommand=sbVer.set)
        self.table()

    def onSave(self):
        entNama = self.inputNama.get()
        entUsername = self.inputUsername.get()
        entPassword = self.inputPassword.get()
        entKonfirmasi = self.inputKonfirmasi.get()
        entBagian = self.inputBagian.get()

        entry_list = []
        entry_list.extend((entNama, entUsername, entPassword, entKonfirmasi, entBagian))

        for entry in enumerate(entry_list):
            if not entNama:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entUsername:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entPassword:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entKonfirmasi:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entBagian:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            else:
                if entPassword != entKonfirmasi:
                    messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
                    break
                else:
                    try:
                        self.create(entNama, entUsername, entPassword, entBagian)
                        self.trvTabel.delete(*self.trvTabel.get_children())
                        self.frame_tabel.after(0, self.table())
                        self.clear()
                    except mysql.connector.errors.IntegrityError:
                        messagebox.showerror(title='Error', message='Username ' + entUsername + ' sudah ada')
                    break
    def onDelete(self):
        konfirmasi_hapus = messagebox.askquestion(title='Hapus data', message='Apakah Anda yakin ingin menghapus?', icon='warning')
        if konfirmasi_hapus == 'yes':
            selected_item = self.trvTabel.selection()[0]
            get_id = self.trvTabel.item(selected_item)['values'][0]
            self.delete(get_id)
            self.trvTabel.delete(*self.trvTabel.get_children())
            self.frame_tabel.after(0, self.table())
            self.onClear()
        else:
            pass

    def onUpdate(self):
        entKode = self.inputKode.get()
        entNama = self.inputNama.get()
        entUsername = self.inputUsername.get()
        entPassword = self.inputPassword.get()
        entKonfirmasi = self.inputKonfirmasi.get()
        entBagian = self.inputBagian.get()

        entry_list = []
        entry_list.extend((entNama, entUsername, entPassword, entKonfirmasi, entBagian))

        for entry in enumerate(entry_list):
            if not entNama:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entUsername:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entPassword:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entKonfirmasi:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entBagian:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            else:
                if entPassword != entKonfirmasi:
                    messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
                    break
                else:
                    self.update(entNama, entUsername, entPassword, entBagian, entKode)
                    self.trvTabel.delete(*self.trvTabel.get_children())
                    self.frame_tabel.after(0, self.table())
                    self.onClear()
                    break

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "2", "4")

        self.trvTabel.column("ID", width=50)
        self.trvTabel.column("Nama", width=250, anchor="w")
        self.trvTabel.column("Username", width=150)
        self.trvTabel.column("Password", width=50)
        self.trvTabel.column("Bagian", width=180)

        result = self.read()
        i=0

        for data in result:
            baris = "genap" if i%2 == 0 else "ganjil"
            self.trvTabel.insert('', 'end', values=data, tags=(baris, ))
            i+=1
        self.trvTabel.tag_configure("ganjil", background="#FFFFFF")
        self.trvTabel.tag_configure("genap", background="whitesmoke")

    def clear(self):
        self.inputKode.config(state='normal')
        self.inputKode.delete(0, END)
        self.inputKode.config(state='readonly')
        self.inputNama.delete(0, END)
        self.inputUsername.delete(0, END)
        self.inputPassword.delete(0, END)
        self.inputKonfirmasi.delete(0, END)
        self.inputBagian.delete(0, END)

    def onClear(self):
        readonlytext = StringVar()
        readonlytext.set('Dikembangkan Otomatis')
        self.clear()
        self.inputKode.config(state='normal', textvariable=readonlytext)
        self.inputKode.config(state='disabled')
        self.updateButton.config(state='disabled')
        self.deleteButton.config(state='disabled')
        self.saveButton.config(state='normal')

    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_admin.py')

    def onDoubleClick(self, event):
        self.saveButton.config(state='disabled')
        self.updateButton.config(state='normal')
        self.deleteButton.config(state='normal')

        self.clear()

        selected = self.trvTabel.focus()
        item = self.trvTabel.item(selected, "values")

        self.inputKode.config(state="normal")
        self.inputKode.insert(END, item[0])
        self.inputKode.config(state='readonly')
        self.inputNama.insert(END, item[1])
        self.inputUsername.insert(END, item[2])
        self.inputPassword.insert(END, item[3])
        self.inputBagian.insert(END, item[4])


Admin(root)
root.mainloop()
