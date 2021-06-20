from tkinter import *
from tkinter import messagebox
from config import Config
import os

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class AdminLogin(Config):
    def __init__(self, toplevel):
        self.toplevel = toplevel
        super(AdminLogin, self).__init__()
        lebar = 350
        tinggi = 370
        setTengahX = (self.toplevel.winfo_screenwidth()-lebar)//2
        setTengahY = (self.toplevel.winfo_screenheight()-tinggi)//2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        #atur frame
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        label_frame = Frame(self.top_level, background='#808080', padx='10', pady='20')
        label_frame.pack(anchor='center', side='top', fill='x')
        input_frame = Frame(self.top_level, background='#cedfe0', padx='20', pady='30')
        input_frame.pack(side='top', fill='both')
        button_frame = Frame(self.top_level, background='#cedfe0', padx='20', pady='5')
        button_frame.pack(side='top', fill='x')

        #atur label
        Label(label_frame, background='#808080', text='Admin Login', font='{Segoe UI Semibold} 14 {}').pack(side='top')
        Label(input_frame, background='#cedfe0', text='USERNAME', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='0')
        Label(input_frame, background='#cedfe0', text='PASSWORD', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='2')

        #atur input
        self.inputUsername = Entry(input_frame, width='50')
        self.inputUsername.grid(column='0', row='1', pady='10')
        self.inputPassword = Entry(input_frame, width='50', show='•')
        self.inputPassword.grid(column='0', row='3', pady='10')

        #button
        self.loginButton = Button(button_frame, font='{Segoe UI Semibold} 11 {}', text='Login', width='33', command=self.proses_login)
        self.loginButton.grid(column='0', row='4', pady='5')
        self.backButton = Button(button_frame, font='{Segoe UI Semibold} 11 {}', text='Kembali', width='33', command=self.onKembali)
        self.backButton.grid(column='0', row='5', pady='5')

    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_admin.py')

    def proses_login(self):
        verifikasi_username = self.inputUsername.get()
        verifikasi_password = self.inputPassword.get()

        if len(verifikasi_username or verifikasi_password) > 0:
            sql = "SELECT username, password FROM admin WHERE username = %s AND password = %s"
            cursor = self._Config__db.cursor()
            cursor.execute(sql, [(verifikasi_username), (verifikasi_password)])
            results = cursor.fetchall()
            if results:
                root.destroy()
                os.system('admin.py')
            else:
                messagebox.showerror(title='Error', message='Username atau Password salah')
        else:
            messagebox.showerror(title='Error', message='Username atau Password tidak boleh kosong')


AdminLogin(root)
root.mainloop()
