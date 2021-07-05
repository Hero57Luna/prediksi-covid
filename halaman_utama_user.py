from tkinter import *
import os

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class UtamaUser:
    def __init__(self, toplevel):
        self.toplevel = toplevel
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

        self.header_label = Label(self.header_frame, background='#808080', text='Halo! Selamat Datang User',
                                  font='{Segoe UI Semibold} 14 {}').pack(side='top')

        self.buttonKelola = Button(self.button_frame, text='Lihat Data Kasus Positif', width='30',
                                   font='{Segoe UI Semibold} 12 {}')
        self.buttonKelola.grid(column='0', row='0', pady='30')
        self.buttonInputData = Button(self.button_frame, text='Input Data Kasus Positif', width='30',
                                      font='{Segoe UI Semibold} 12 {}')
        self.buttonInputData.grid(column='0', row='1', pady='30')
        self.buttonPrediksi = Button(self.button_frame, text='Lakukan Prediksi Data', width='30',
                                     font='{Segoe UI Semibold} 12 {}')
        self.buttonPrediksi.grid(column='0', row='2', pady='30')

UtamaUser(root)
root.mainloop()