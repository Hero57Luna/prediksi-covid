from tkinter import *
from tkinter import messagebox
from config import Config
import os, glob

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0, 0)
root.iconbitmap("Polinema.ico")

class GantiPassword(Config):
    def __init__(self, toplevel):
        self.toplevel = toplevel

        super(GantiPassword, self).__init__()
        lebar = 400
        tinggi = 350
        setTengahX = (self.toplevel.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.toplevel.winfo_screenheight() - tinggi) // 2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        label_frame = Frame(self.top_level, background='#808080', padx='10', pady='20')
        label_frame.pack(anchor='center', side='top', fill='x')
        input_frame = Frame(self.top_level, background='#cedfe0', padx='20', pady='30')
        input_frame.pack(side='top', fill='both')
        button_frame = Frame(self.top_level, background='#cedfe0')
        button_frame.pack(side='top')

        Label(label_frame, background='#808080', text='Ganti Password', font='{Segoe UI Semibold} 14 {}').pack(side='top')
        Label(input_frame, background='#cedfe0', text='ID Anda', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='0', sticky='w')
        Label(input_frame, background='#cedfe0', text='Password Lama', font='{Segoe UI Semibold} 12 {}').grid(column='0', row='1', sticky='w')
        Label(input_frame, background='#cedfe0', text='Password Baru', font='{Segoe UI Semibold} 12 {}').grid(
            column='0', row='2', sticky='w')
        Label(input_frame, background='#cedfe0', text='Konfirmasi', font='{Segoe UI Semibold} 12 {}').grid(
            column='0', row='3', sticky='w')

        id_user = StringVar()
        id_user.set(self.readpass())
        self.idEntry = Entry(input_frame, textvariable=id_user, state='readonly')
        self.idEntry.grid(column='1', row='0', sticky='w', padx='20')
        self.oldPassword = Entry(input_frame, show='•')
        self.oldPassword.grid(column='1', row='1', sticky='w', padx='20')
        self.newPassword = Entry(input_frame, show='•')
        self.newPassword.grid(column='1', row='2', sticky='w', padx='20')
        self.konfirmasi = Entry(input_frame, show='•')
        self.konfirmasi.grid(column='1', row='3', sticky='w', padx='20')

        self.saveButton = Button(button_frame, font='{Segoe UI Semibold} 10 {}', text='Simpan', command=self.gantiPassword)
        self.saveButton.grid(column='0', row='0', padx='5')
        self.kembaliButton = Button(button_frame, font='{Segoe UI Semibold} 10 {}', text='Kembali', command=self.delete_pass)
        self.kembaliButton.grid(column='1', row='0')


    def onKembali(self):
        root.destroy()
        os.system('admin.py')

    def readpass(self):
        fname = 'pass.txt'
        with open(fname) as f:
            for line in f:
                return line

    def gantiPassword(self):
        cursor = self._Config__db.cursor()
        getID = self.idEntry.get()
        getOldPassword = self.oldPassword.get()
        getNewPassword = self.newPassword.get()
        getKonfirmasi = self.konfirmasi.get()

        #get id user inside login table
        select_id = "SELECT * FROM login WHERE id_user = '{}'".format(getID)
        cursor.execute(select_id)
        result_id = cursor.fetchone()

        #get password from login
        select_password = "SELECT password FROM login WHERE id_user = '{}'".format(getID)
        cursor.execute(select_password)
        result_password = cursor.fetchone()

        entry_list = [getID, getOldPassword, getNewPassword, getKonfirmasi]

        for entry in enumerate(entry_list):
            if not getID:
                messagebox.showerror(title='Error', message='Field harus lengkap')
                break
            if not getOldPassword:
                messagebox.showerror(title='Error', message='Field harus lengkap')
                break
            if not getNewPassword:
                messagebox.showerror(title='Error', message='Field harus lengkap')
                break
            if not getKonfirmasi:
                messagebox.showerror(title='Error', message='Field harus lengkap')
                break
            else:
                if getNewPassword != getKonfirmasi:
                    messagebox.showerror(title='Error', message='Password dengan konfirmasi tidak sama')
                    break
                elif result_id:
                    if result_password[0] == getOldPassword:
                        self.changePassword(getNewPassword, getID)
                        self.delete_pass()
                    else:
                        messagebox.showerror(title='Error', message='User dengan password tersebut tidak terdaftar')
                    break
                else:
                    messagebox.showerror(title='Error', message='User tidak terdaftar')
                    break

    def delete_pass(self):
        fname = 'pass.txt'
        filelist = glob.glob(fname)
        for f in filelist:
            os.remove(f)
        root.destroy()
        os.system('admin.py')


GantiPassword(root)
root.mainloop()