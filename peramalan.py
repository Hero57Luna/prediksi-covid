from datetime import datetime
import pandas as pd
from tkinter import *
from tkinter import ttk
from operator import itemgetter
from matplotlib import pyplot as plt
import numpy as np

root = Tk()
root.title('Halaman Prediksi')
root.resizable(0,0)

class Peramalan:

    df = pd.read_csv('Positif.csv', parse_dates=True)
    i = 0

    def __init__(self, toplevel):
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
        Label(self.top_level, background='#cedfe0', text='Halaman Prediksi', font='{Segoe UI Semibold} 16 {}').pack(side='top', fill='x')
        self.nilai_frame = Frame(self.top_level, background='#cedfe0')
        self.nilai_frame.pack(side='top', fill='both')
        self.button_frame = Frame(self.top_level, background='#cedfe0', pady='50')
        self.button_frame.pack(side='top', fill='both')


        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Nilai Error\t:').grid(column='0', row='0', padx='30', pady='10', sticky='w')
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

        Button(self.button_frame, command=self.single_exponential_smoothing,font='{Segoe UI Semibold} 10 {}', relief='groove', text='Generate Graph', width='20').grid(column='0', padx='30', row='0', sticky='w')

    def single_exponential_smoothing(self):
        alpha = 0.5
        hasil = []
        error = []
        data_terakhir =self.df['Kasus'].tail(1)
        baca_kasus = self.df['Kasus']
        baca_tanggal = pd.to_datetime(self.df['Tanggal'], format='%d-%b-%Y')
        tanggal_to_array = np.array(baca_tanggal)
        kasus_to_array = np.array(baca_kasus)
        jumlah_hari = baca_tanggal.count()


        for i in range(jumlah_hari):
            kasus = baca_kasus.values[i]
            t_plus_one = self.df['Kasus'].shift(1).values[i]
            F_ke_n = (alpha * t_plus_one) + (1 - alpha) * kasus
            hasil.append(F_ke_n)
            error.append(F_ke_n - t_plus_one)



        sum_error = sum(error[1:])
        mean_error = sum(error[1:])/jumlah_hari
        squared_difference = np.square(error[1:])
        add_squared = np.nansum(squared_difference)
        mean_squared_error = add_squared/jumlah_hari

        forecast_terakhir = hasil[-1]

        prediksi_besok = (alpha * data_terakhir) + (1 - alpha) * forecast_terakhir
        prediksi_besok = int(prediksi_besok)

        # masukkan forecast
        copy_hasil = hasil.copy()
        copy_hasil.insert(len(copy_hasil), prediksi_besok)
        print(copy_hasil)

        #MAPE
        mape = np.nanmean(np.abs((kasus_to_array[1:] - hasil[1:])/kasus_to_array[1:])) * 100
        nilai_mape = "{:.2f}".format(mape)

        self.inputError.config(state='normal')
        self.inputMSE.config(state='normal')
        self.inputPrediksi.config(state='normal')
        self.inputAkurasi.config(state='normal')

        self.inputError.insert(END, mean_error)
        self.inputMSE.insert(END, mean_squared_error)
        self.inputPrediksi.insert(END, prediksi_besok)
        self.inputAkurasi.insert(END, nilai_mape)

        self.inputError.config(state='readonly')
        self.inputMSE.config(state='readonly')
        self.inputPrediksi.config(state='readonly')
        self.inputAkurasi.config(state='readonly')




        #plot data
        fig, ax = plt.subplots()
        ax.plot(tanggal_to_array[1:], copy_hasil[1:], label='Ramalan')
        ax.plot(tanggal_to_array, kasus_to_array, label='Aktual')
        plt.legend()
        plt.show()






Peramalan(root)
root.mainloop()


