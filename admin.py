from tkinter import *
from tkinter import ttk, messagebox
from config import Config
import os
import glob
import subprocess
import mysql.connector

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")
# config = Config()
judul_kolom = ("ID", "Nama", "Telepon", "Username", "Password", "Role", "UserDelete", "Status")
optionlist = ["ADM", "USR"]
entries_field = []


class Admin(Config):
    def __init__(self, parent):
        super(Admin, self).__init__()
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.delete_credentials)
        lebar = 800
        tinggi = 705
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        #atur frame
        self.top_level = Frame(self.parent, background='#cedfe0')
        self.top_level.pack(side=TOP, fill=BOTH)
        Label(self.top_level, background='#808080', font='{Segoe UI Semibold} 14 {}', text='Halaman Kelola Pengguna', padx='10', pady='20').pack(fill='x', side='top')
        input_frame = Frame(self.top_level, background='#cedfe0')
        input_frame.pack(side=TOP, fill=X)
        self.frame_button = Frame(self.top_level, background='#cedfe0')
        self.frame_button.pack(side=TOP, fill=BOTH, padx='20')
        self.frame_tabel = Frame(self.top_level, background='#cedfe0')
        self.frame_tabel.pack(fill='both', padx=5, pady=5)
        self.frame_menu = Frame(self.top_level, background='#cedfe0')
        self.frame_menu.pack(side=TOP, fill='y', pady='20')

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
        self.searchEntry = Entry(self.frame_button, font='{Calibri} 13 {}')
        self.searchEntry.grid(column='5', row='0', padx='5')


        #button frame
        self.saveButton = Button(self.frame_button, command=self.onSave, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Simpan', width='8')
        self.saveButton.grid(column='0', padx='10', pady='20', row='0', sticky='w')
        self.updateButton = Button(self.frame_button, font='{Segoe UI Semibold} 10 {}', relief='groove', state='disabled', text='Update', width='8', command=self.onUpdate)
        self.updateButton.grid(column='1', padx='10', pady='20', row='0', sticky='w')
        self.deleteButton = Button(self.frame_button, command=self.onDelete, state='disabled', font='{Segoe UI Semibold} 10 {}', relief='groove', text='Hapus', width='8')
        self.deleteButton.grid(column='2', row='0', padx='10', pady='20', sticky='w')
        self.activateUser = Button(self.frame_button, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Aktifkan User', width='13', command=self.onActivateUser, state='disabled')
        self.activateUser.grid(column='3', row='0')
        self.clearButton = Button(self.frame_button, font='{Segoe UI Semibold} 10 {}', command=self.onClear, relief='groove', text='Clear', width='8')
        self.clearButton.grid(column='4', row='0', sticky='w', padx='10')
        self.searchButton = Button(self.frame_button, font='{Segoe UI Semibold} 9 {}', relief='groove', text='Cari', command=self.onSearch)
        self.searchButton.grid(column='6', row='0', sticky='e')
        self.resetButton = Button(self.frame_button, font='{Segoe UI Semibold} 9 {}', relief='groove', text='Reset', command=self.reset, state='disabled')
        self.resetButton.grid(column='7', row='0', sticky='e')
        self.backButton = Button(self.frame_menu, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Kembali', width='8', command=self.onKembali)
        self.backButton.grid(column='0', row='0', padx='10')
        self.changePassword = Button(input_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Ganti Password', state='disabled', command=self.onChangePassword)
        self.changePassword.grid(column='2', row='3', sticky='w')

        #tabel
        self.trvTabel = ttk.Treeview(self.frame_tabel, columns=judul_kolom, show='headings')
        self.trvTabel.bind("<Double-1>", self.onDoubleClick)
        sbVer = Scrollbar(self.frame_tabel)
        sbVer.pack(side=RIGHT, fill=Y)
        self.trvTabel.pack(fill=BOTH)
        sbVer.config(command=self.trvTabel.yview)
        self.table()

    def onSave(self):
        entNama = self.inputNama.get()
        entTelepon = self.inputTelepon.get()
        entPassword = self.inputPassword.get()
        entKonfirmasi = self.inputKonfirmasi.get()
        entUsername = self.inputUsername.get()
        entRole = self.value_inside.get()

        if not entNama:
            messagebox.showerror(title="Error", message="Nama harus diisi")
        elif not entTelepon:
            messagebox.showerror(title="Error", message="Telepon harus diisi")
        elif not entPassword:
            messagebox.showerror(title="Error", message="Password harus diisi")
        elif not entKonfirmasi:
            messagebox.showerror(title="Error", message="Konfirmasi harus diisi")
        elif not entUsername:
            messagebox.showerror(title="Error", message="Username harus diisi")
        elif entRole == "Pilih role Anda":
            messagebox.showerror(title="Error", message="Isikan role Anda")
        elif entPassword != entKonfirmasi:
            messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
        else:
            try:
                self.create(entNama, entTelepon, entRole, entUsername, entPassword)
                self.trvTabel.delete(*self.trvTabel.get_children())
                self.frame_tabel.after(0, self.table())
                self.onClear()
            except mysql.connector.errors.IntegrityError as e:
                if e.errno == 1062:
                    messagebox.showerror(title='Error', message='Username sudah ada')

    def onDelete(self):
        konfirmasi_hapus = messagebox.askquestion(title='Hapus data', message='Apakah Anda yakin ingin menghapus?', icon='warning')
        if konfirmasi_hapus == 'yes':
            selected_item = self.trvTabel.selection()[0]
            get_id = self.trvTabel.item(selected_item)['values'][0]
            self.deactivate_user(get_id)
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

        if not entNama:
            messagebox.showerror(title="Error", message="Nama harus diisi")
        elif not entTelepon:
            messagebox.showerror(title="Error", message="Telepon harus diisi")
        elif not entPassword:
            messagebox.showerror(title="Error", message="Password harus diisi")
        elif not entKonfirmasi:
            messagebox.showerror(title="Error", message="Konfirmasi harus diisi")
        elif not entUsername:
            messagebox.showerror(title="Error", message="Username harus diisi")
        elif not entRole:
            messagebox.showerror(title="Error", message="Isikan role Anda")
        elif entPassword != entKonfirmasi:
            messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
        elif entPassword != entKonfirmasi:
                messagebox.showerror(title="Error", message="Konfirmasi Password Tidak Sama")
        else:
            self.update(entNama, entUsername, entPassword, entTelepon, entRole, entKode)
            self.trvTabel.delete(*self.trvTabel.get_children())
            self.frame_tabel.after(0, self.table())
            self.onClear()

    def onActivateUser(self):
        selected_item = self.trvTabel.selection()[0]
        get_id = self.trvTabel.item(selected_item)['values'][0]
        self.activate_user(get_id)
        self.trvTabel.delete(*self.trvTabel.get_children())
        self.frame_tabel.after(0, self.table())

    def onSearch(self):
        searchIndex = self.searchEntry.get()
        if len(searchIndex) > 0:
            self.resetButton.config(state='normal')
            self.searchEntry.delete(0, END)
            for record in self.trvTabel.get_children():
                self.trvTabel.delete(record)

            result = self.search_user(searchIndex)

            for data in result:
                self.trvTabel.insert('', 'end', values=data)
        else:
            pass

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "2", "3", "5", "7")

        self.trvTabel.column("ID", anchor=CENTER,width=50, stretch=NO)
        self.trvTabel.column("Nama", width=205, stretch=NO)
        self.trvTabel.column("Telepon", width=150, stretch=NO)
        self.trvTabel.column("Password", width=100, stretch=NO)
        self.trvTabel.column("Username", width=150, stretch=NO)
        self.trvTabel.column("Role", anchor=CENTER, width=96, stretch=NO)
        self.trvTabel.column("UserDelete", width=100, stretch=NO)
        self.trvTabel.column("Status", width=120, stretch=NO)

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
        kode = self.inputKode.get()
        f = open("pass.txt", "w")
        f.write(kode)
        subprocess.check_call(['attrib', '+H', 'pass.txt'])
        f.close()
        root.destroy()
        os.system('halaman_ganti_password.py')

    def onDoubleClick(self, event):
        self.saveButton.config(state='disabled')
        self.updateButton.config(state='normal')
        self.deleteButton.config(state='normal')

        self.clear()

        selected = self.trvTabel.focus()
        item = self.trvTabel.item(selected, "values")
        user_status = []

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
        user_status.insert(0, item[6])
        if user_status[0] == 'None':
            self.activateUser.config(state='disabled')
        else:
            self.activateUser.config(state='normal')

    def reset(self):
        for record in self.trvTabel.get_children():
            self.trvTabel.delete(record)
        self.table()
        self.resetButton.config(state='disabled')

    def delete_credentials(self):
        dir = os.getcwd()
        target = dir + '\credentials.cred'
        filelist = glob.glob(target)
        for f in filelist:
            os.remove(f)
        root.quit()


Admin(root)
root.mainloop()
