import pandas as pd
from tkinter import *
from tkinter import messagebox
from matplotlib import pyplot as plt
import numpy as np
import os
from config import Config

root = Tk()
root.title("Prediksi Covid v.1.0")
root.resizable(0,0)
root.iconbitmap("Polinema.ico")

class Peramalan(Config):

    def __init__(self, toplevel):
        super(Peramalan, self).__init__()
        self.toplevel = toplevel
        lebar = 600
        tinggi = 500
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

        Button(self.button_frame, command=self.GenerateGraph,font='{Segoe UI Semibold} 10 {}', relief='groove', text='Generate Graph', width='20').grid(column='0', padx='10', row='0')
        self.buttonPreVaksin = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Prediksi Pre-Vaksin', width='20', command=self.PreVaksin)
        self.buttonPreVaksin.grid(column='0', row='1', padx='10')
        self.buttonGenerateCSV = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Generate CSV', width='20', command=self.onGenerateCSV)
        self.buttonGenerateCSV.grid(column='1', row='0', padx='10')
        self.buttonPascaVaksin = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Prediksi Pasca Vaksin', width='20', command=self.PascaVaksin)
        self.buttonPascaVaksin.grid(column='1', row='1', padx='10', pady='10')
        self.buttonKembali = Button(self.button_frame, font='{Segoe UI Semibold} 10 {}', relief='groove', text='Kembali', width='8', command=self.onKembali)
        self.buttonKembali.grid(column='0', row='2', columnspan='2', pady='10')

    def onKembali(self):
        root.destroy()
        os.system('halaman_utama_user.py')

    def onGenerateCSV(self):
       self.GenerateAllData()

    def GenerateGraph(self):
        try:
            np.set_printoptions(precision=3, suppress=True)
            cwd = os.getcwd()
            target_file = '\exported\Positif.csv'
            target_dir = cwd + target_file
            df = pd.read_csv(target_dir, parse_dates=True)
            alpha = 0.9
            kasus = df['Kasus']
            tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
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

            plt.plot(tanggal, final, label='Ramalan')
            plt.plot(tanggal, kasus, label='Aktual')
            plt.legend()
            plt.show()
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File data tidak ditemukan')

    def PreVaksin(self):
        try:
            np.set_printoptions(precision=3, suppress=True)
            cwd = os.getcwd()
            target_file = '\exported\DataPreVaksin.csv'
            target_dir = cwd + target_file
            df = pd.read_csv(target_dir, parse_dates=True)
            alpha = 0.9
            kasus = df['Kasus']
            tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
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

            # hitung mean error
            copy_forecast = final.copy()
            copy_kasus = kasus_to_array.copy()
            forecast_error = copy_forecast[:-1]
            kasus_error = copy_kasus[1:]
            error = np.subtract(kasus_error, forecast_error)
            mean_error = np.abs(np.nansum(error))
            mean_error = '%.3f' % mean_error

            # hitung mse
            squared_difference = error ** 2
            sum_squared_difference = np.nansum(squared_difference)
            mse = sum_squared_difference / jumlah_data
            mse = '%.3f' % mse


            # hitung MAPE
            mape = np.nansum(np.abs((kasus_to_array - final) / np.nansum(kasus_to_array))) * 100
            mape = "{:.0f}".format(mape) + "%"

            # prediksi periode berikutnya
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

            plt.plot(tanggal, final, label='Ramalan Pre Vaksin')
            plt.legend()
            plt.show()
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File data tidak ditemukan')

    def PascaVaksin(self):
        try:
            np.set_printoptions(precision=3, suppress=True)
            cwd = os.getcwd()
            target_file = '\exported\DataPascaVaksin.csv'
            target_dir = cwd + target_file
            df = pd.read_csv(target_dir, parse_dates=True)
            alpha = 0.9
            kasus = df['Kasus']
            tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
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

            # hitung mean error
            copy_forecast = final.copy()
            copy_kasus = kasus_to_array.copy()
            forecast_error = copy_forecast[:-1]
            kasus_error = copy_kasus[1:]
            error = np.subtract(kasus_error, forecast_error)
            mean_error = np.abs(np.nansum(error))
            mean_error = '%.3f' % mean_error


            # hitung mse
            squared_difference = error ** 2
            sum_squared_difference = np.nansum(squared_difference)
            mse = sum_squared_difference / jumlah_data
            mse = '%.3f' % mse


            # hitung MAPE
            mape = np.nansum(np.abs((kasus_to_array - final) / np.nansum(kasus_to_array))) * 100
            mape = "{:.0f}".format(mape) + "%"

            # prediksi periode berikutnya
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

            plt.plot(tanggal, final, label='Ramalan Pasca Vaksin')
            plt.legend()
            plt.show()
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File data tidak ditemukan')

Peramalan(root)
root.mainloop()