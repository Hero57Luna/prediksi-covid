from tkinter import *

root = Tk()
root.title('Halaman Utama Admin')
root.resizable(0, 0)


class UtamaAdmin:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        lebar = 600
        tinggi = 500
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
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='50')
        self.button_frame.pack(side='top')

        #label
        self.header_label = Label(self.header_frame, background='#808080', text='Halo! Selamat Datang', font='{Segoe UI Semibold} 14 {}').pack(side='top')

        #button
        self.buttonKelola = Button(self.button_frame, text='Kelolah Pengguna', width='30', font='{Segoe UI Semibold} 12 {}', command=self.KelolaPengguna)
        self.buttonKelola.grid(column='0', row='0', pady='50')
        self.buttonInputData = Button(self.button_frame, text='Input Data Kasus Positif', width='30', font='{Segoe UI Semibold} 12 {}')
        self.buttonInputData.grid(column='0', row='1', pady='50')

    def KelolaPengguna(self):
        root.destroy()
        import admin

    def InputDataPositif(self):
        pass


UtamaAdmin(root)
root.mainloop()
