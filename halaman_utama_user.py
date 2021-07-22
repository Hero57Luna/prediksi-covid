from tkinter import *
import os, glob

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class UtamaUser:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.protocol("WM_DELETE_WINDOW", self.delete_credentials)
        lebar = 600
        tinggi = 500
        setTengahX = (self.toplevel.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.toplevel.winfo_screenheight() - tinggi) // 2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        # frame
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        self.header_frame = Frame(self.top_level, background='#808080', padx='10', pady='20')
        self.header_frame.pack(side='top', fill='x', anchor='center')
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='10')
        self.button_frame.pack(side='top')

        self.header_label = Label(self.header_frame, background='#808080', text='Halo User {}\n Selamat Datang'.format(self.read_credentials()),
                                  font='{Segoe UI Semibold} 14 {}').pack(side='top')

        self.buttonLihatKasus = Button(self.button_frame, text='Lihat Data Kasus Positif', width='30',
                                   font='{Segoe UI Semibold} 12 {}', command=self.lihatKasus)
        self.buttonLihatKasus.grid(column='0', row='0', pady='30')
        self.buttonInputData = Button(self.button_frame, text='Input Data Kasus Positif', width='30',
                                      font='{Segoe UI Semibold} 12 {}', command=self.inputPositif)
        self.buttonInputData.grid(column='0', row='1', pady='30')
        self.buttonPrediksi = Button(self.button_frame, text='Lakukan Prediksi Data', width='30',
                                     font='{Segoe UI Semibold} 12 {}', command=self.prediksiKasus)
        self.buttonPrediksi.grid(column='0', row='2', pady='30')

    def lihatKasus(self):
        root.destroy()
        os.system('halaman_lihat_kasus_positif.py')

    def inputPositif(self):
        root.destroy()
        os.system('halaman_input_positif.py')

    def prediksiKasus(self):
        root.destroy()
        os.system('peramalan.py')

    def read_credentials(self):
        fname = 'credentials.cred'
        with open(fname) as f:
            for line in f:
                hasil = line.split(',')
                return hasil[0]

    def delete_credentials(self):
        dir = os.getcwd()
        target = dir + '\credentials.cred'
        filelist = glob.glob(target)
        for f in filelist:
            os.remove(f)
        root.quit()

UtamaUser(root)
root.mainloop()