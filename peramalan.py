import pandas as pd
from tkinter import *
from matplotlib import pyplot as plt
import numpy as np
import os
from config import Config
from sklearn.metrics import mean_absolute_percentage_error

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


        Label(self.nilai_frame, background='#cedfe0', font='{Segoe UI Semibold} 12 {}', text='Mean Error\t:').grid(column='0', row='0', padx='30', pady='10', sticky='w')
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

        Button(self.button_frame, command=self.single_exponential_smoothing,font='{Segoe UI Semibold} 10 {}', relief='groove', text='Generate Graph', width='20').grid(column='0', padx='10', row='0')
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
        os.system('python halaman_utama_admin.py')

    def onGenerateCSV(self):
       self.GenerateAllData()

    def single_exponential_smoothing(self):
        cwd = os.getcwd()
        target_file = '\exported\Positif.csv'
        target_dir = cwd + target_file
        df = pd.read_csv(target_dir, parse_dates=True)
        alpha = 0.1
        hasil = []
        error = []
        t_plus_one_error = []
        data_terakhir = df['Kasus'].tail(1)
        baca_kasus = df['Kasus']
        baca_tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
        tanggal_to_array = np.array(baca_tanggal)
        kasus_to_array = np.array(baca_kasus)
        jumlah_hari = baca_tanggal.count()


        for i in range(jumlah_hari):
            kasus = baca_kasus.values[i]
            t_plus_one = df['Kasus'].shift(1).values[i]
            F_ke_n = (alpha * t_plus_one) + (1 - alpha) * kasus
            hasil.append(F_ke_n)
            t_plus_one_error.append(t_plus_one)
            error.append(F_ke_n - t_plus_one)


        mean_error = np.nansum(error)/jumlah_hari

        #hitung MSE
        squared_difference = np.square(error[1:])
        add_squared = np.nansum(squared_difference)
        mean_squared_error = add_squared/jumlah_hari

        forecast_terakhir = hasil[-1]

        prediksi_besok = (alpha * data_terakhir) + (1 - alpha) * forecast_terakhir
        prediksi_besok = int(prediksi_besok)

        # masukkan forecast
        copy_hasil = hasil.copy()
        copy_hasil.insert(len(copy_hasil), prediksi_besok)
        # print(copy_hasil)

        #MAPE
        mape = np.nanmean(np.abs((kasus_to_array[1:] - hasil[1:])/kasus_to_array[1:])) * 100
        print(mape)
        nilai_mape = "{:.2f}".format(mape)

        ujimape = mean_absolute_percentage_error(kasus_to_array[1:], hasil[1:])
        print(ujimape)



        self.inputError.config(state='normal')
        self.inputMSE.config(state='normal')
        self.inputPrediksi.config(state='normal')
        self.inputAkurasi.config(state='normal')

        self.inputError.delete(0, END)
        self.inputMSE.delete(0, END)
        self.inputPrediksi.delete(0, END)
        self.inputAkurasi.delete(0, END)

        self.inputError.insert(END, mean_error)
        self.inputMSE.insert(END, mean_squared_error)
        self.inputPrediksi.insert(END, prediksi_besok)
        self.inputAkurasi.insert(END, nilai_mape+'%')

        self.inputError.config(state='readonly')
        self.inputMSE.config(state='readonly')
        self.inputPrediksi.config(state='readonly')
        self.inputAkurasi.config(state='readonly')

        plt.plot(tanggal_to_array, hasil, label='Ramalan')
        plt.plot(tanggal_to_array, kasus_to_array, label='Aktual')
        plt.legend()
        plt.show()

    def PreVaksin(self):
        cwd = os.getcwd()
        target_file = '\exported\DataPreVaksin.csv'
        target_dir = cwd + target_file
        df = pd.read_csv(target_dir, parse_dates=True)
        alpha = 0.1
        hasil = []
        error = []
        t_plus_one_error = []
        data_terakhir = df['Kasus'].tail(1)
        baca_kasus = df['Kasus']
        baca_tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
        tanggal_to_array = np.array(baca_tanggal)
        kasus_to_array = np.array(baca_kasus)
        jumlah_hari = baca_tanggal.count()

        for i in range(jumlah_hari):
            kasus = baca_kasus.values[i]
            t_plus_one = df['Kasus'].shift(1).values[i]
            F_ke_n = (alpha * t_plus_one) + (1 - alpha) * kasus
            hasil.append(F_ke_n)
            t_plus_one_error.append(t_plus_one)
            error.append(F_ke_n - t_plus_one)

        mean_error = np.nansum(error) / jumlah_hari

        # hitung MSE
        squared_difference = np.square(error[1:])
        add_squared = np.nansum(squared_difference)
        mean_squared_error = add_squared / jumlah_hari

        forecast_terakhir = hasil[-1]

        prediksi_besok = (alpha * data_terakhir) + (1 - alpha) * forecast_terakhir
        prediksi_besok = int(prediksi_besok)

        # masukkan forecast
        copy_hasil = hasil.copy()
        copy_hasil.insert(len(copy_hasil), prediksi_besok)
        # print(copy_hasil)

        # MAPE
        mape = np.nanmean(np.abs((kasus_to_array[1:] - hasil[1:]) / kasus_to_array[1:])) * 100
        print(mape)
        nilai_mape = "{:.2f}".format(mape)

        ujimape = mean_absolute_percentage_error(kasus_to_array[1:], hasil[1:])
        print(ujimape)

        self.inputError.config(state='normal')
        self.inputMSE.config(state='normal')
        self.inputPrediksi.config(state='normal')
        self.inputAkurasi.config(state='normal')

        self.inputError.delete(0, END)
        self.inputMSE.delete(0, END)
        self.inputPrediksi.delete(0, END)
        self.inputAkurasi.delete(0, END)

        self.inputError.insert(END, mean_error)
        self.inputMSE.insert(END, mean_squared_error)
        self.inputPrediksi.insert(END, prediksi_besok)
        self.inputAkurasi.insert(END, nilai_mape + '%')

        self.inputError.config(state='readonly')
        self.inputMSE.config(state='readonly')
        self.inputPrediksi.config(state='readonly')
        self.inputAkurasi.config(state='readonly')

        plt.plot(tanggal_to_array, hasil, label='Ramalan Pre-Vaksin')
        plt.legend()
        plt.show()

    def PascaVaksin(self):
        cwd = os.getcwd()
        target_file = '\exported\DataPascaVaksin.csv'
        target_dir = cwd + target_file
        df = pd.read_csv(target_dir, parse_dates=True)
        alpha = 0.1
        hasil = []
        error = []
        t_plus_one_error = []
        data_terakhir = df['Kasus'].tail(1)
        baca_kasus = df['Kasus']
        baca_tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
        tanggal_to_array = np.array(baca_tanggal)
        kasus_to_array = np.array(baca_kasus)
        jumlah_hari = baca_tanggal.count()

        for i in range(jumlah_hari):
            kasus = baca_kasus.values[i]
            t_plus_one = df['Kasus'].shift(1).values[i]
            F_ke_n = (alpha * t_plus_one) + (1 - alpha) * kasus
            hasil.append(F_ke_n)
            t_plus_one_error.append(t_plus_one)
            error.append(F_ke_n - t_plus_one)

        mean_error = np.nansum(error) / jumlah_hari

        # hitung MSE
        squared_difference = np.square(error[1:])
        add_squared = np.nansum(squared_difference)
        mean_squared_error = add_squared / jumlah_hari

        forecast_terakhir = hasil[-1]

        prediksi_besok = (alpha * data_terakhir) + (1 - alpha) * forecast_terakhir
        prediksi_besok = int(prediksi_besok)

        # masukkan forecast
        copy_hasil = hasil.copy()
        copy_hasil.insert(len(copy_hasil), prediksi_besok)
        # print(copy_hasil)

        # MAPE
        mape = np.nanmean(np.abs((kasus_to_array[1:] - hasil[1:]) / kasus_to_array[1:])) * 100
        print(mape)
        nilai_mape = "{:.2f}".format(mape)

        ujimape = mean_absolute_percentage_error(kasus_to_array[1:], hasil[1:])
        print(ujimape)

        self.inputError.config(state='normal')
        self.inputMSE.config(state='normal')
        self.inputPrediksi.config(state='normal')
        self.inputAkurasi.config(state='normal')

        self.inputError.delete(0, END)
        self.inputMSE.delete(0, END)
        self.inputPrediksi.delete(0, END)
        self.inputAkurasi.delete(0, END)

        self.inputError.insert(END, mean_error)
        self.inputMSE.insert(END, mean_squared_error)
        self.inputPrediksi.insert(END, prediksi_besok)
        self.inputAkurasi.insert(END, nilai_mape + '%')

        self.inputError.config(state='readonly')
        self.inputMSE.config(state='readonly')
        self.inputPrediksi.config(state='readonly')
        self.inputAkurasi.config(state='readonly')

        plt.plot(tanggal_to_array, hasil, label='Ramalan Pasca Vaksin')
        plt.legend()
        plt.show()

Peramalan(root)
root.mainloop()