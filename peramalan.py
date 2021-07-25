import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk
from matplotlib import pyplot as plt
import numpy as np
import os
import glob
from config import Config

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0,0)
root.iconbitmap("Polinema.ico")
judul_kolom = ("Tanggal", "Prediksi Besok", "MAE", "MAPE", "Dimasukkan Oleh")

class Peramalan(Config):
    def __init__(self, toplevel):
        super(Peramalan, self).__init__()
        self.toplevel = toplevel
        self.toplevel.protocol("WM_DELETE_WINDOW", self.delete_credentials)
        lebar = 620
        tinggi = 700
        setTengahX = (self.toplevel.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.toplevel.winfo_screenheight() - tinggi) // 2
        self.toplevel.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
        self.komponen()

    def komponen(self):
        #atur frame
        self.top_level = Frame(self.toplevel, background='#cedfe0')
        self.top_level.pack(side='top', fill='both', expand='true')
        Label(self.top_level, background='#808080', text='Halaman Prediksi', font='{Segoe UI Semibold} 14 {}', padx='10', pady='20').pack(side='top', fill='both')
        self.nilai_frame = Frame(self.top_level, background='#cedfe0')
        self.nilai_frame.pack(side='top', fill='both')
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='20', padx='10')
        self.button_frame.pack(side='top')
        self.tabel_frame = Frame(self.top_level, background='#cedfe0')
        self.tabel_frame.pack(fill='both', padx=5, pady=5)
        self.menu_frame = Frame(self.top_level, background='#cedfe0')
        self.menu_frame.pack(side=TOP, fill='y', pady='20')


        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='MAE\t\t:').grid(column='0', row='0', padx='30', pady='10', sticky='w')
        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Nilai MSE\t\t:').grid(
            column='0', row='1', padx='30', pady='10', sticky='w')
        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Prediksi Besok\t:').grid(
            column='0', row='2', padx='30', pady='10', sticky='w')
        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='MAPE\t\t: ').grid(
            column='0', row='3', padx='30', pady='10', sticky='w')

        self.inputError = Entry(self.nilai_frame, state='readonly')
        self.inputError.grid(column='1', row='0')
        self.inputMSE = Entry(self.nilai_frame, state='readonly')
        self.inputMSE.grid(column='1', row='1')
        self.inputPrediksi = Entry(self.nilai_frame, state='readonly')
        self.inputPrediksi.grid(column='1', row='2')
        self.inputAkurasi = Entry(self.nilai_frame, state='readonly')
        self.inputAkurasi.grid(column='1', row='3')

        Button(self.button_frame, command=self.GenerateGraph, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Prediksi Data', width='20').grid(column='0', padx='10', row='0')
        self.buttonPreVaksin = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Prediksi Pre-Vaksin', width='20', command=self.PreVaksin)
        self.buttonPreVaksin.grid(column='0', row='1', padx='10')
        self.buttonGenerateCSV = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Generate CSV', width='20', command=self.onGenerateCSV)
        self.buttonGenerateCSV.grid(column='1', row='0', padx='10')
        self.buttonPascaVaksin = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Prediksi Pasca Vaksin', width='20', command=self.PascaVaksin)
        self.buttonPascaVaksin.grid(column='1', row='1', padx='10', pady='10')
        self.buttonSimpan = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Simpan', command=self.onSave)
        self.buttonSimpan.grid(column='2', row='0')
        self.buttonKembali = Button(self.menu_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Kembali', width='8', command=self.onKembali)
        self.buttonKembali.grid(column='0', row='0', columnspan='2', pady='10')

        self.trvTabel = ttk.Treeview(self.tabel_frame, columns=judul_kolom, show='headings')
        sbVer = Scrollbar(self.tabel_frame)
        sbVer.pack(side=RIGHT, fill=Y)
        self.trvTabel.pack(fill=BOTH)
        sbVer.config(command=self.trvTabel.yview)
        self.table()

    def read_credentials(self):
        fname = 'credentials.cred'
        with open(fname) as f:
            for line in f:
                hasil = line.split(',')
                return hasil[0]

    def onSave(self):
        try:
            credentials = self.read_credentials()
            cwd = os.getcwd()
            target_file = '\exported\Positif.csv'
            target_dir = cwd + target_file
            df = pd.read_csv(target_dir, parse_dates=True)
            tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y').dt.date
            besok = pd.DatetimeIndex(tanggal) + pd.DateOffset(1)
            esok = besok[-1]
            MAE = self.inputError.get()
            MAPE = self.inputAkurasi.get()
            prediksi = self.inputPrediksi.get()
            self.insertRamalan(iduser=credentials, tanggal=esok, prediksi=prediksi, mae=MAE, mape=MAPE)
            self.trvTabel.delete(*self.trvTabel.get_children())
            self.tabel_frame.after(0, self.table())
        except FileNotFoundError as e:
            if e.errno == 2:
                messagebox.showerror(title='Error', message='Credentials tidak ditemukan, harap login untuk menyimpan data')


    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_user.py')

    def onGenerateCSV(self):
       self.GenerateAllData()

    def forecasting(self, namafile, ramalan, aktual):
        try:
            np.set_printoptions(precision=3, suppress=True)
            cwd = os.getcwd()
            target_file = '\exported\{}.csv'.format(namafile)
            target_dir = cwd + target_file
            df = pd.read_csv(target_dir, parse_dates=True)
            alpha = 0.9
            kasus = df['Kasus']
            tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y').dt.date
            hasil = []
            jumlah_data = kasus.count()

            for i, x in enumerate(kasus):
                if i == 0:
                    res = x
                    hasil.append(x)
                else:
                    tmp = alpha * x + (1 - alpha) * res
                    hasil.append(tmp)
                    res = tmp

            final = np.array(hasil)
            kasus_to_array = np.array(kasus)


            #hitung mean error
            copy_forecast = final.copy()
            copy_kasus = kasus_to_array.copy()
            forecast_error = copy_forecast[:-1]
            kasus_error = copy_kasus[1:]
            error = np.subtract(kasus_error, forecast_error)
            mean_error = np.abs(np.nansum(error))
            mean_error = '%.3f' % mean_error

            #hitung mse
            squared_difference = error**2
            sum_squared_difference = np.nansum(squared_difference)
            mse = sum_squared_difference / jumlah_data
            mse = '%.3f' % mse

            #hitung MAPE
            mape = np.nansum(np.abs((kasus_to_array - final)/np.nansum(kasus_to_array))) * 100
            mape = "{:.0f}".format(mape) + "%"

            #prediksi periode berikutnya
            next_period = int(final[-1])
            next_period_to_str = str(next_period) + ' orang'

            self.inputError.config(state='normal')
            self.inputMSE.config(state='normal')
            self.inputPrediksi.config(state='normal')
            self.inputAkurasi.config(state='normal')

            self.inputError.delete(0, END)
            self.inputMSE.delete(0, END)
            self.inputPrediksi.delete(0, END)
            self.inputAkurasi.delete(0, END)

            self.inputError.insert(END, mean_error)
            self.inputMSE.insert(END, mse)
            self.inputPrediksi.insert(END, next_period_to_str)
            self.inputAkurasi.insert(END, mape)

            self.inputError.config(state='readonly')
            self.inputMSE.config(state='readonly')
            self.inputPrediksi.config(state='readonly')
            self.inputAkurasi.config(state='readonly')

            plt.plot(tanggal, final, label='{}'.format(ramalan))
            plt.plot(tanggal, kasus, label='{}'.format(aktual))
            plt.legend()
            plt.show()
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File data tidak ditemukan')

    def GenerateGraph(self):
        self.forecasting(namafile='Positif', ramalan='Ramalan', aktual='Aktual')

    def PreVaksin(self):
        self.forecasting('DataPreVaksin', ramalan='Ramalan Pre Vaksin', aktual='Pre Vaksin Aktual')

    def PascaVaksin(self):
        self.forecasting('DataPascaVaksin', ramalan='Ramalan Pasca Vaksin', aktual='Pasca Vaksin Aktual')

    def SmadaKraskaan(self):
        self.forecasting(namafile='smadakraksaan', ramalan='Ramalan', aktual='Aktual')

    def delete_credentials(self):
        dir = os.getcwd()
        target = dir + '\credentials.cred'
        filelist = glob.glob(target)
        for f in filelist:
            os.remove(f)
        root.quit()

    def table(self):
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel["displaycolumns"]=("0", "1", "2", "3", "4")

        self.trvTabel.column("Tanggal", width=150,anchor=CENTER, stretch=NO)
        self.trvTabel.column("Prediksi Besok", width=100,anchor=CENTER, stretch=NO)
        self.trvTabel.column("MAE", width=60,anchor=CENTER, stretch=NO)
        self.trvTabel.column("MAPE", width=60,anchor=CENTER, stretch=NO)
        self.trvTabel.column("Dimasukkan Oleh", width=220,anchor=CENTER, stretch=NO)

        ramalan_result = self.read_ramalan()

        for data in ramalan_result:
            self.trvTabel.insert('', 'end', values=data)

Peramalan(root)
root.mainloop()