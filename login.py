from tkinter import *
from tkinter import messagebox
from config import Config
import os, glob, subprocess
from pathlib import Path

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")


class Login(Config):

    def __init__(self, toplevel):
        # root.protocol("WM_DELETE_WINDOW", self.delete_credentials)
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
            sql = "SELECT id, username, level, user_delete FROM user WHERE username = '{0}' AND password = '{1}'".format(verifikasi_username, verifikasi_password)
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                if str(results[3]) == 'None':
                    if results[2] == 'ADM':
                        self.credentials()
                        root.destroy()
                        os.system('halaman_utama_admin.py')
                    elif results[2] == 'USR':
                        self.credentials()
                        root.destroy()
                        os.system('halaman_utama_user.py')
                else:
                    messagebox.showerror(title='Error', message='Pengguna ini tidak lagi aktif, hubungi Admin untuk lebih lanjut')
            else:
                messagebox.showerror(title='Error', message='Pengguna ini tidak ditemukan')
            # val = (verifikasi_username, verifikasi_password)
            # sql = "SELECT id_user FROM login WHERE sandi = '{0}' AND username = '{1}'".format(verifikasi_password, verifikasi_username)
            # cursor.execute(sql)
            # results = cursor.fetchone()
            # if results:
            #     user_query = "SELECT role, user_delete FROM user WHERE id = '{}'".format(results[0])
            #     cursor.execute(user_query)
            #     hasil_user = cursor.fetchone()
            #     if hasil_user[0] == 'ADM':
            #        if str(hasil_user[1]) == 'None':
            #            self.credentials()
            #            root.destroy()
            #            os.system('halaman_utama_admin.py')
            #        else:
            #            messagebox.showerror(title='Error', message='Pengguna ini tidak lagi aktif, kontak admin untuk informasi lebih lanjut')
            #     elif hasil_user[0] == 'USR':
            #         if str(hasil_user[1]) == 'None':
            #             self.credentials()
            #             root.destroy()
            #             os.system('halaman_utama_user.py')
            #         else:
            #             messagebox.showerror(title='Error', message='Pengguna ini tidak lagi aktif, kontak admin untuk informasi lebih lanjut')
            # else:
            #     messagebox.showerror(title='Error', message='Username atau Password Anda salah')
        else:
            messagebox.showerror(title='Error', message='Username atau Password tidak boleh kosong')

    def credentials(self):
        path = Path('.').absolute() / 'credentials.cred'
        target = '%r'%str(path)
        cursor = self._Config__db.cursor()
        verifikasi_username = self.inputUsername.get()
        verifikasi_password = self.inputPassword.get()
        sql = "SELECT id, level, nama " \
              "FROM user " \
              "WHERE username = '{0}' AND password = '{1}' " \
              "INTO OUTFILE {2} " \
              "FIELDS TERMINATED BY ',' " \
              r"LINES TERMINATED BY '\n'".format(verifikasi_username, verifikasi_password, target)
        cursor.execute(sql)
        subprocess.check_call(['attrib', '+H', 'credentials.cred'])

    def delete_credentials(self):
        dir = os.getcwd()
        target = dir + '\credentials.cred'
        filelist = glob.glob(target)
        for f in filelist:
            os.remove(f)
        root.quit()


Login(root)
root.mainloop()