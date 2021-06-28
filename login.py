from tkinter import *
from tkinter import messagebox
from config import Config
import os

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class Login(Config):
    def __init__(self, toplevel):
        self.toplevel = toplevel
        super(Login, self).__init__()
        lebar = 350
        tinggi = 500
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
        header_frame = Frame(self.top_level, background='#cedfe0', padx='10', pady='20')
        header_frame.pack(anchor='center', side='top', fill='x')
        input_frame = Frame(self.top_level, background='#cedfe0', padx='20', pady='30')
        input_frame.pack(side='top', fill='both')
        button_frame = Frame(self.top_level, background='#cedfe0', padx='20', pady='20')
        button_frame.pack(side='top', fill='x')

        #atur label
        Label(label_frame, background='#808080', text='Login', font='{Segoe UI Semibold} 14 {}').pack(side='top')
        Label(header_frame, background='#cedfe0', text='Silahkan lakukan login \n terlebih dahulu', font='{Segoe UI Semibold} 16 {}').pack(side='top')
        Label(input_frame, background='#cedfe0', text='USERNAME', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='0')
        Label(input_frame, background='#cedfe0', text='PASSWORD', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='2')

        #atur input
        self.inputUsername = Entry(input_frame, width='50')
        self.inputUsername.grid(column='0', row='1', pady='10')
        self.inputPassword = Entry(input_frame, width='50', show='•')
        self.inputPassword.grid(column='0', row='3', pady='10')

        #button
        self.loginButton = Button(button_frame, font='{Segoe UI Semibold} 11 {}', text='Login', width='33', command=self.proses_login)
        self.loginButton.grid(column='0', row='4')

    def login_gagal(self):
        pass

    def proses_login(self):
        cursor = self._Config__db.cursor()
        verifikasi_username = self.inputUsername.get()
        verifikasi_password = self.inputPassword.get()
        if len(verifikasi_username or verifikasi_password) > 0:
            sql = "SELECT id_user FROM login WHERE username = '{}' AND password = '{}'".format(verifikasi_username,
                                                                                               verifikasi_password)
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                user_query = "SELECT role FROM user WHERE id = {}".format(results[0])
                cursor.execute(user_query)
                hasil_user = cursor.fetchone()
                if hasil_user[0] == 'ADM':
                    root.destroy()
                    os.system('halaman_utama_admin.py')
                elif hasil_user[0] == 'USR':
                    root.destroy()
                    os.system('halaman_utama_user.py')
            else:
                print("User tidak ditemukan")
        else:
            messagebox.showerror(title='Error', message='Username atau Password tidak boleh kosong')


Login(root)
root.mainloop()