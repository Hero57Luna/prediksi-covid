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
judul_kolom = ("ID", "Nama", "Telepon", "Username", "Password", "Role")
optionlist = ["ADM", "USR"]


class Admin(Config):
    def __init__(self, parent):
        super(Admin, self).__init__()
        self.parent = parent
        lebar = 700
        tinggi = 705
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))

        self.komponen()

    def komponen(self):
        #atur frame
        top_level = Frame(self.parent, background='#cedfe0')
        top_level.pack(side=TOP, fill=BOTH)
        Label(top_level, background='#808080', font='{Segoe UI Semibold} 14 {}', text='Halaman Kelola Pengguna', padx='10', pady='20').pack(fill='x', side='top')
        input_frame = Frame(top_level, background='#cedfe0')
        input_frame.pack(side=TOP, fill=X)
        self.frame_button = Frame(top_level, background='#cedfe0')
        self.frame_button.pack(side=TOP, fill=X)
        self.frame_tabel = Frame(top_level)
        self.frame_tabel.pack(side=TOP, fill='both', expand=YES, padx=5, pady=5)
        self.frame_menu = Frame(top_level, background='#cedfe0')
        self.frame_menu.pack(side=TOP, fill='y', expand=YES)

        #input frame_label
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Kode').grid(column='0', padx='30', pady='5', row='0', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Nama').grid(column='0', padx='30', pady='5', row='1', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Telepon').grid(column='0', padx='30', pady='5', row='2', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Password').grid(column='0', padx='30', pady='5', row='3', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Konfirmasi Password').grid(column='0', padx='30', pady='5', row='4', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Username').grid(column='0', padx='30', pady='5', row='5', sticky='w')
        Label(input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Role').grid(column='0', padx='30', pady='5', row='6', sticky='w')

        self.value_inside = StringVar(root)
        self.value_inside.set("Pilih role Anda")

        #input frame entry
        readonlytext = StringVar()
        readonlytext.set('Dikembangkan Otomatis')
        self.inputKode = Entry(input_frame, width='25', state='normal', textvariable=readonlytext)
        self.inputKode.grid(column='1', padx='20', row='0', sticky='w')
        self.inputKode.config(state='disabled')
        self.inputNama = Entry(input_frame, width='30')
        self.inputNama.grid(column='1', padx='20', row='1', sticky='w')
        self.inputTelepon = Entry(input_frame, width='20')
        self.inputTelepon.grid(column='1', padx='20', row='2', sticky='w')
        self.inputPassword = Entry(input_frame, width='25', show='•')
        self.inputPassword.grid(column='1', padx='20', row='3', sticky='w')
        self.inputKonfirmasi = Entry(input_frame, width='25', show='•')
        self.inputKonfirmasi.grid(column='1', padx='20', row='4', sticky='w')
        self.inputUsername = Entry(input_frame, width='25')
        self.inputUsername.grid(column='1', padx='20', row='5', sticky='w')
        self.inputRole = OptionMenu(input_frame, self.value_inside, *optionlist)
        self.inputRole.grid(column='1', padx='20', row='6', sticky='w')


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
        self.changePassword = Button(input_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Ganti Password', state='disabled', command=self.onChangePassword)
        self.changePassword.grid(column='2', row='3', sticky='w')

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
        entTelepon = self.inputTelepon.get()
        entPassword = self.inputPassword.get()
        entKonfirmasi = self.inputKonfirmasi.get()
        entUsername = self.inputUsername.get()
        entRole = self.value_inside.get()

        entry_list = []
        entry_list.extend((entNama, entTelepon, entPassword, entKonfirmasi, entUsername, entRole))

        for entry in enumerate(entry_list):
            if not entNama:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entTelepon:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entPassword:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entKonfirmasi:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entUsername:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entRole:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            else:
                if entPassword != entKonfirmasi:
                    messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
                    break
                else:
                    try:
                        self.create(entNama, entTelepon, entRole, entUsername, entPassword)
                        self.trvTabel.delete(*self.trvTabel.get_children())
                        self.frame_tabel.after(0, self.table())
                        self.onClear()
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
        entTelepon = self.inputTelepon.get()
        entPassword = self.inputPassword.get()
        entKonfirmasi = self.inputKonfirmasi.get()
        entUsername = self.inputUsername.get()
        entRole = self.value_inside.get()

        entry_list = []
        entry_list.extend((entNama, entTelepon, entPassword, entKonfirmasi, entUsername, entRole))

        for entry in enumerate(entry_list):
            if not entNama:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entTelepon:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entPassword:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entKonfirmasi:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entUsername:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            if not entRole:
                messagebox.showerror(title="Error", message="Field harus lengkap")
                break
            else:
                if entPassword != entKonfirmasi:
                    messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
                    break
                else:
                    self.update(entNama, entTelepon, entRole, entUsername, entPassword, entKode)
                    self.trvTabel.delete(*self.trvTabel.get_children())
                    self.frame_tabel.after(0, self.table())
                    self.onClear()
                    break

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "2", "3", "5")

        self.trvTabel.column("ID", anchor=CENTER,width=50, stretch=NO)
        self.trvTabel.column("Nama", width=205, stretch=NO)
        self.trvTabel.column("Telepon", width=150, stretch=NO)
        self.trvTabel.column("Password", width=100, stretch=NO)
        self.trvTabel.column("Username", width=150, stretch=NO)
        self.trvTabel.column("Role", anchor=CENTER, width=96, stretch=NO)

        user_result = self.read_user()
        i=0

        for data_user in user_result:
            self.trvTabel.insert('', 'end', values=data_user)
            i+=1

    def clear(self):
        self.inputKode.config(state='normal')
        self.inputKode.delete(0, END)
        self.inputKode.config(state='readonly')
        self.inputNama.delete(0, END)
        self.inputTelepon.delete(0, END)
        self.inputUsername.delete(0, END)
        self.inputPassword.config(state='normal')
        self.inputPassword.delete(0, END)
        self.inputKonfirmasi.delete(0, END)


    def onClear(self):
        readonlytext = StringVar()
        readonlytext.set('Dikembangkan Otomatis')
        self.clear()
        self.inputKode.config(state='normal', textvariable=readonlytext)
        self.inputKode.config(state='disabled')
        self.updateButton.config(state='disabled')
        self.deleteButton.config(state='disabled')
        self.saveButton.config(state='normal')
        self.changePassword.config(state='disabled')

    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_admin.py')

    def onChangePassword(self):
        root.destroy()
        os.system('halaman_ganti_password.py')

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
        self.inputTelepon.insert(END, item[2])
        self.inputUsername.insert(END, item[3])
        self.inputPassword.insert(END, item[4])
        self.inputPassword.config(state='readonly')
        self.value_inside.set(item[5])
        self.changePassword.config(state='normal')


Admin(root)
root.mainloop()
