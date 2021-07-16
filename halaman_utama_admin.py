from tkinter import *
from tkinter import messagebox
import os, glob

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class UtamaAdmin:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.protocol("WM_DELETE_WINDOW", self.delete_credentials)
        lebar = 600
        tinggi = 400
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
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='10')
        self.button_frame.pack(side='top')

        #label
        self.header_label = Label(self.header_frame, background='#808080', text='Halo admin {}Selamat Datang'.format(self.read_credentials()), font='{Segoe UI Semibold} 14 {}').pack(side='top')

        #button
        self.buttonKelola = Button(self.button_frame, text='Kelolah Pengguna', width='30', font='{Segoe UI Semibold} 12 {}', command=self.KelolaPengguna)
        self.buttonKelola.grid(column='0', row='0', pady='30')
        self.lihatDataPositif = Button(self.button_frame, text='Lihat Kasus Positif COVID-19', width='30', font='{Segoe UI Semibold} 12 {}', command=self.lihatDataPositif)
        self.lihatDataPositif.grid(column='0', row='1', pady='30')

    def KelolaPengguna(self):
        root.destroy()
        os.system('admin.py')

    def lihatDataPositif(self):
        root.destroy()
        os.system('halaman_lihat_kasus_positif.py')

    def read_credentials(self):
        fname = 'credentials.cred'
        with open(fname) as f:
            next(f)
            for line in f:
                return line

    def delete_credentials(self):
        dir = os.getcwd()
        target = dir + '\credentials.cred'
        filelist = glob.glob(target)
        for f in filelist:
            os.remove(f)
        root.quit()

UtamaAdmin(root)
root.mainloop()
