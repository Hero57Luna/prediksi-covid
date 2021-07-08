from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
from config import Config
import datetime

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")
judul_kolom = ("Tanggal", "Kasus", "UserID", "Nama")

class InputPositif(Config):

    def __init__(self, toplevel):
        super(InputPositif, self).__init__()
        self.toplevel = toplevel
        lebar = 500
        tinggi = 600
        setTengahX = (self.toplevel.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.toplevel.winfo_screenheight() - tinggi) // 2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        #frame
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        self.header_frame = Frame(self.top_level, background='#808080', padx='10', pady='20')
        self.header_frame.pack(side='top', fill='x', anchor='center')
        self.input_frame = Frame(self.top_level, background='#cedfe0')
        self.input_frame.pack(side='top', fill='x')
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='10')
        self.button_frame.pack(side='top', fill='both', padx='20')
        self.frame_tabel = Frame(self.top_level, background='#cedfe0')
        self.frame_tabel.pack(fill='both', padx='10', pady='10')

        #label
        self.header_label = Label(self.header_frame, background='#808080', text='Halaman Input Kasus Positif', font='{Segoe UI Semibold} 14 {}')
        self.header_label.pack(side='top')
        Label(self.input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Tanggal').grid(column='0', padx='30', pady='5', row='0', sticky='w')
        Label(self.input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='(YYYY-MM-DD)').grid(column='2', row='0', sticky='w', padx='30', pady='5')
        Label(self.input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Jumlah Kasus').grid(row='2', column='0', padx='30', pady='5', sticky='w')
        Label(self.input_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='ID Anda').grid(column='0', row='3', padx='30', pady='5', sticky='w')

        #entry field
        self.entryTanggal = Entry(self.input_frame)
        self.entryTanggal.grid(row='0', column='1', padx='10')
        self.entryKasus = Entry(self.input_frame)
        self.entryKasus.grid(row='2', column='1')
        self.entryUsername = Entry(self.input_frame)
        self.entryUsername.grid(row='3', column='1')

        #tabel
        sbVer = Scrollbar(self.frame_tabel)
        sbVer.pack(side=RIGHT, fill=Y)
        self.trvTabel = ttk.Treeview(self.frame_tabel, yscrollcommand=sbVer.set, columns=judul_kolom, show='headings')
        self.trvTabel.bind("<Double-1>", self.onDoubleClick)
        self.trvTabel.pack(fill=BOTH)
        sbVer.config(command=self.trvTabel.yview)
        self.table()

        #button
        self.saveButton = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Simpan', command=self.onSave, width='8')
        self.saveButton.grid(row='0', column='0', padx='5', pady='10', sticky='w')
        self.updateButton = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Update', width='8')
        self.updateButton.grid(row='0', column='1', padx='5', pady='10', sticky='w')
        self.deleteButton = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Hapus', width='8')
        self.deleteButton.grid(row='0', column='2', padx='5', pady='10', sticky='w')

    def onSave(self):
        entTanggal = self.entryTanggal.get()
        entKasus = self.entryKasus.get()
        entUsername = self.entryUsername.get()
        #konversi tanggal dan kasus
        tanggalString = str(entTanggal)
        format = "%Y-%m-%d"

        if len(entTanggal or entKasus) > 0 :
            if len(entTanggal) > 0 :
                if len(entKasus) > 0 :
                    try:
                        kasusInt = int(entKasus)
                        datetime.datetime.strptime(tanggalString, format)
                        konfirmasi = messagebox.askquestion(title='Konfirmasi', message='Tanggal {} dengan kasus {} orang \n Apkah sudah benar?'.format(entTanggal, entKasus))
                        if konfirmasi == 'yes':
                            try:
                                self.insertKasus(entTanggal, kasusInt, entUsername)
                                self.onClear()
                                messagebox.showinfo(title='Sukses', message='Data berhasil dimasukkan')
                                self.trvTabel.delete(*self.trvTabel.get_children())
                                self.frame_tabel.after(0, self.table())
                            except mysql.connector.errors.IntegrityError as e:
                                if e.errno == 1062:
                                    messagebox.showerror(title="Error", message="Tanggal {} sudah ada".format(entTanggal))
                                elif e.errno == 1452:
                                    messagebox.showerror(title="Error", message="User tidak terdaftar")
                        else:
                            pass
                    except ValueError:
                        messagebox.showerror(title='Error', message='Mohon cek kembali format tanggal dan kasus')
                else:
                    messagebox.showerror(title='Error',message='Kasus tidak boleh kosong')
            else:
                messagebox.showerror(title='Error', message='Tanggal tidak boleh kosong')
        else:
            messagebox.showerror(title='Error', message='Field tidak boleh kosong')

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "3")

        self.trvTabel.column("Tanggal", anchor=CENTER, width=110, stretch=NO)
        self.trvTabel.column("Kasus", anchor=CENTER, width=90, stretch=NO)
        self.trvTabel.column("UserID", anchor=CENTER, width=261, stretch=NO)
        self.trvTabel.column("Nama", anchor=CENTER, width=261, stretch=NO)

        result = self.read_positif()

        for data in result:
            self.trvTabel.insert('', 'end', values=data)

    def onDoubleClick(self, event):
        self.onClear()

        selected = self.trvTabel.focus()
        item = self.trvTabel.item(selected, "values")

        self.entryTanggal.insert(END, item[0])
        self.entryKasus.insert(END, item[1])
        self.entryUsername.insert(END, item[2])

    def onClear(self):
        self.entryTanggal.delete(0, END)
        self.entryKasus.delete(0, END)
        self.entryUsername.delete(0, END)

    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_admin.py')

InputPositif(root)
root.mainloop()