from tkinter import *
from tkinter import ttk, messagebox
from config import Config
import os
import mysql.connector

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")
judul_kolom = ("Tanggal", "Jumlah Kasus", "UserID", "Nama")

class LihatPositif(Config):

    def __init__(self, toplevel):
        super(LihatPositif, self).__init__()
        self.toplevel = toplevel
        lebar = 500
        tinggi = 600
        setTengahX = (self.toplevel.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.toplevel.winfo_screenheight() - tinggi) // 2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        self.header_frame = Frame(self.top_level, background='#808080', padx='10', pady='20')
        self.header_frame.pack(side='top', fill='x', anchor='center')
        self.seacrhFrame = Frame(self.top_level, background='#cedfe0')
        self.seacrhFrame.pack(anchor='e', padx='10')
        self.frame_tabel = Frame(self.top_level, background='#cedfe0')
        self.frame_tabel.pack(padx='10', fill=BOTH)
        self.informasi_frame = Frame(self.top_level, background='#cedfe0')
        self.informasi_frame.pack(side='top', expand='yes', fill='both', pady='10', padx='10')

        Label(self.header_frame, background='#808080', text='Halaman Informasi Kasus Positif', font='{Segoe UI Semibold} 14 {}').pack()

        self.searchEntry = Entry(self.seacrhFrame)
        self.searchEntry.grid(column='0', row='0')
        self.searchButton = Button(self.seacrhFrame, font='{Segoe UI Semibold} 7 {}',  relief='groove', text='Cari', width='5', command=self.search)
        self.searchButton.grid(column='1', row='0', padx='5', pady='5')
        self.resetButton = Button(self.seacrhFrame, font='{Segoe UI Semibold} 7 {}', relief='groove', text='Reset',
                                   width='5', state='disabled', command=self.reset)
        self.resetButton.grid(column='2', row='0', pady='5')

        sbVer = Scrollbar(self.frame_tabel)
        sbVer.pack(side=RIGHT, fill=Y)

        self.trvTabel = ttk.Treeview(self.frame_tabel, yscrollcommand=sbVer.set, columns=judul_kolom, show='headings')
        self.trvTabel.pack(fill=BOTH)

        sbVer.config(command=self.trvTabel.yview)
        self.table()


        Label(self.informasi_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Jumlah data\t\t').grid(column='0', row='0', sticky='w')
        Label(self.informasi_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Total Kasus').grid(
            column='0', row='1', sticky='w')
        Label(self.informasi_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Input data terakhir').grid(
            column='0', row='2', sticky='w')
        Label(self.informasi_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Jumlah kasus tertinggi').grid(
            column='0', row='3', sticky='w')
        Label(self.informasi_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Jumlah kasus terendah').grid(
            column='0', row='4', sticky='w')

        varlist = {var: StringVar() for var in ["jumlahData", "totalKasus", "lastInput", "kasusTertinggi", "kasusTerendah"]}
        varlist["jumlahData"].set(self.read_jumlah_data())
        varlist["totalKasus"].set(self.read_total_kasus())
        varlist["kasusTertinggi"].set(self.kasus_terbesar())
        varlist["kasusTerendah"].set(self.kasus_terkecil())

        last_element = self.read_positif()[-1]
        varlist["lastInput"].set(last_element[3])

        self.jumlahDataEntry = Entry(self.informasi_frame, state='readonly', textvariable=varlist["jumlahData"])
        self.jumlahDataEntry.grid(column='1', row='0')
        self.totalKasusEntry = Entry(self.informasi_frame, state='readonly', textvariable=varlist["totalKasus"])
        self.totalKasusEntry.grid(column='1', row='1')
        self.lastInputEntry = Entry(self.informasi_frame, state='readonly', textvariable=varlist["lastInput"])
        self.lastInputEntry.grid(column='1', row='2')
        self.highestCaseEntry = Entry(self.informasi_frame, state='readonly', textvariable=varlist["kasusTertinggi"])
        self.highestCaseEntry.grid(column='1', row='3')
        self.lowestCaseEntry = Entry(self.informasi_frame, state='readonly', textvariable=varlist["kasusTerendah"])
        self.lowestCaseEntry.grid(column='1', row='4')

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "3")

        self.trvTabel.column("Tanggal", anchor=CENTER, width=110)
        self.trvTabel.column("Jumlah Kasus", anchor=CENTER, width=90)
        self.trvTabel.column("UserID", anchor=CENTER, width=261)
        self.trvTabel.column("Nama", anchor=CENTER, width=261)

        result = self.read_positif()

        for data in result:
            self.trvTabel.insert('', 'end', values=data)

    def search(self):
        searchIndex = self.searchEntry.get()
        if len(searchIndex) > 0:
            self.resetButton.config(state='normal')
            self.searchEntry.delete(0, END)
            for record in self.trvTabel.get_children():
                self.trvTabel.delete(record)

            result = self.search_kasus(searchIndex)

            for data in result:
                self.trvTabel.insert('', 'end', values=data)
        else:
            pass

    def reset(self):
        for record in self.trvTabel.get_children():
            self.trvTabel.delete(record)
        self.table()
        self.resetButton.config(state='disabled')


LihatPositif(root)
root.mainloop()