from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
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

data = pd.read_csv('Positif.csv')


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
kasus = data['Kasus']

F2 = (0.4 * 9) + (1 - 0.4) * 8
print(F2)

F3 = (0.4 * 15) + (1 - 0.4) * F2
print(F3)

F4 = (0.4 * 26) + (1 - 0.4) * F3
print(F4)

forecast = [F2, F3, F4]

plt.plot_date(data['Tanggal'].head(3), kasus.head(3), linestyle='solid')
plt.plot_date(data['Tanggal'].head(3), forecast, linestyle='solid')

plt.tight_layout()

plt.show()


# bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei']
# penjualan = [2100, 2031, 1000, 2651, 3210]
#
# plt.plot(bulan, penjualan)
# plt.xlabel('Bulan')
# plt.ylabel('Penjualan')
# plt.title('Data Penjualan')
#
# plt.show()