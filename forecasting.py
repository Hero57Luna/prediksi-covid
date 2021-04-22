from datetime import datetime
import pandas as pd
from operator import itemgetter
from matplotlib import pyplot as plt

import numpy as np

df = pd.read_csv('Positif.csv', parse_dates=True)

i = 0
j = 1
time = []
#count = df['Tanggal'].count()
kasus = df['Kasus']
alpha = 0.5
ramalan = []
error = []
error_squared = []
ramalan1 = []
tanggal = df['Tanggal']
tanggal = pd.to_datetime(df['Tanggal'], format='%d-%b-%Y')
bulan = tanggal.count()
kasus_aktual = df['Kasus']
one_month = pd.DateOffset(months=2)
time = tanggal + one_month
data = df.set_index(time)
counter = time.count()
kakulasi = []
kalkulasi1 = []

for i in range(bulan):
    kasus = df['Kasus'].values[i]
    t_plus_one = df['Kasus'].shift(1).values[i]
    forecast = (alpha * t_plus_one) + (1 - alpha) * kasus
    result = forecast[~np.isnan(forecast)]
    forecast1 = (alpha * t_plus_one) + (1 - alpha) * forecast
    ramalan1.append(forecast1)
    error.append(forecast1 - t_plus_one)

array_error = np.array(error)
vertical_error = np.vstack(array_error)
mean_error = np.nansum(array_error)
mean_squared_error = np.power(array_error, 2)
mean_squared_error1 = np.nansum(mean_squared_error)
print(mean_error/144)
print(mean_squared_error1/144)
print(ramalan1)


get_last_value = df['Kasus'].tail(1)
get_last_forecast = ramalan1[-1]
rumus = (alpha * get_last_value) + (1 - alpha) * get_last_forecast
last_forecast = np.array(rumus)


j = 0
ramal = []
ramal2 = []

rumus1 = (alpha * last_forecast) + (1 - alpha) * last_forecast



data1 = pd.DataFrame(ramalan1)
data1.columns = ['Ramalan']
ramalan11 = np.array(data1)
array_tanggal = np.array(tanggal)

def hitung_mape(At, Ft):
    At = np.array(At)
    Ft = np.array(Ft)
    return np.nanmean(np.abs((At - Ft) / At)) * 100

data_as_array = df['Kasus'].values[1:]
print(hitung_mape(data_as_array, data1[1:]))




# print(ramalan1)
# print(len(time))
# data1 = pd.DataFrame(ramalan1)
# data1.columns = ['Ramalan']
# ramalan11 = np.array(data1)
# array_tanggal = np.array(tanggal)


# fig, ax = plt.subplots()
# ax.plot(tanggal, kasus_aktual, label='Kasus Aktual', color='blue')
# ax.plot(array_tanggal, ramalan11, label='Ramalan', color='red')
# plt.plot(tanggal, data1, label='Prediksi')
# # data.plot()
# plt.plot(tanggal, kasus_aktual, label='Aktual')
# plt.plot(time, kasus_aktual,'b',time, data1, 'r--')
# df_all = pd.merge(kasus_aktual, data1, how='inner', left_index=True, right_index=True)
# df_all.plot(useOffset=True)
# plt.legend()
# plt.show()

# data = {'Error':[error]}
# df1 = pd.DataFrame(data)
# print(df1)


























# kasus = data['Kasus']

# F2 = (0.4 * 9) + (1 - 0.4) * 8
# print(F2)
#
# F3 = (0.4 * 15) + (1 - 0.4) * F2
# print(int(F3))
#
# F4 = (0.4 * 26) + (1 - 0.4) * F3
# print(int(F4))
#
# forecast = [F2, F3, F4]
#
# plt.plot(data['Tanggal'].head(3), kasus.head(3), linestyle='solid')
# plt.plot(data['Tanggal'].head(3), forecast, linestyle='solid')
#
# plt.tight_layout()
#
# plt.show()























# bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei']
# penjualan = [2100, 2031, 1000, 2651, 3210]
#
# plt.plot(bulan, penjualan)
# plt.xlabel('Bulan')
# plt.ylabel('Penjualan')
# plt.title('Data Penjualan')
#
# plt.show()

import csv

from matplotlib.dates import DateFormatter

# with open('Positif.csv') as csv_file:
#     csv_reader = csv.reader(csv_file)
#
#     next(csv_reader)
#
#     tanggal = []
#     kasus = []
#
#     for line in csv_reader:
#         tanggal.append(line[0])
#         kasus.append(line[1])

# data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%d-%b')
# data.set_index('Tanggal', inplace=True)
# data.resample('1M').count()['Kasus'].plot()
# final_data = data.groupby(pd.Grouper(freq='M'))

#data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%d-%b-%Y')

#data['Tanggal'] = data.groupby(pd.Grouper(freq='M')).sum()
# kasus = data['Kasus']


# kasus = data['Kasus']
# tanggal =

# plt.plot(final_data)
# plt.gcf().autofmt_xdate()
# date_format = DateFormatter('%d-%m')
# plt.gca().xaxis.set_major_formatter(date_format)


#tanggal = data['Tanggal']
