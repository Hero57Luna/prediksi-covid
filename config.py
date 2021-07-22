import mysql.connector
import os, glob
import sys
import mysql.connector.locales.eng.client_error
from tkinter import messagebox
import ctypes
from pathlib import Path

class Config(object):

    # this is the database connection configuration

    def __init__(self):
        self.__host = "localhost"
        self.__username = "root"
        self.__password = ""
        self.__database = "sisfo-covid"
        try:
            self.buatKoneksi()
        except mysql.connector.Error:
            ICON_STOP = 0x10
            ctypes.windll.user32.MessageBoxW(0, "Database Anda tidak terhubung, harap cek koneksi Database Anda", "Error", ICON_STOP)
            sys.exit(0)

    def buatKoneksi(self):
        db = mysql.connector.connect(
            host = self.__host,
            user = self.__username,
            password = self.__password,
            database = self.__database
        )
        self.__db = db

    def koneksiDB(self):
        konek = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "sisfo-covid"
        }

        try:
            c = mysql.connector.connect(konek)
            return c
        except mysql.connector.errors.InterfaceError:
            print("Sambungan gagal")
            exit(1)

    # end for database connection block

    # create is used for the purpose of data insert for pengguna
    def create(self, nama, telepon, level, username, password):
        self.nama = nama
        self.telepon = telepon
        self.username = username
        self.password = password
        self.level = level
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO user (nama, username, password, telepon, level) "
                       "VALUES('{0}', '{1}', '{2}', '{3}', '{4}');"
                       .format(nama, username, password, telepon, level))
        self.__db.commit()

    def insertKasus(self, tanggal, jumlah, username):
        cursor = self.__db.cursor()
        value = (tanggal, jumlah, username)
        cursor.execute("INSERT INTO datakasus (Tanggal, Kasus, username) VALUES (%s, %s, %s)", value)
        self.__db.commit()

    def insertRamalan(self, iduser, tanggal, prediksi, mae, mape):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO dataramalan (id_user, tanggal, prediksibesok, mae, mape) VALUES ({0},'{1}','{2}','{3}', '{4}')".format(iduser, tanggal, prediksi, mae, mape))
        self.__db.commit()
    # end for insertion

    # read_kasus is used in the halaman input positif
    # the difference between read_kasus vs read_positif are as follows:
    # read_kasus needs the datakasus id for CUD operation whereas read_positif isn't
    def read_kasus(self):
        cur = self.__db.cursor()
        cur.execute("SELECT datakasus.id, datakasus.Tanggal, datakasus.Kasus, datakasus.username, user.nama FROM datakasus INNER JOIN user ON datakasus.username=user.id GROUP BY Tanggal ASC")
        data_kasus = cur.fetchall()
        return data_kasus

    def read_positif(self):
        cur = self.__db.cursor()
        cur.execute("SELECT datakasus.Tanggal, datakasus.Kasus, datakasus.username, user.nama FROM datakasus INNER JOIN user ON datakasus.username=user.id GROUP BY Tanggal ASC")
        data_positif = cur.fetchall()
        return data_positif

    def read_ramalan(self):
        cur = self.__db.cursor()
        cur.execute("SELECT dataramalan.tanggal, dataramalan.prediksibesok, dataramalan.mae, dataramalan.mape, user.nama FROM dataramalan INNER JOIN user ON dataramalan.id_user=user.id")
        results = cur.fetchall()
        return results

    # the blocks below are used for the purpose of read
    # rad_user is used for well you guessed it, read the user(user, admin)
    def read_user(self):
        cur = self.__db.cursor()
        cur.execute("SELECT id, nama, telepon, username, "
                    "password, level, user_delete,"
                    "CASE WHEN user_delete IS NULL THEN 'User Aktif'"
                    "ELSE 'User Tidak Aktif'"
                    "END AS StatusKaryawan "
                    "FROM user;")
        data_user = cur.fetchall()
        return data_user

    def kasus_terbesar(self):
        cur = self.__db.cursor()
        cur.execute("SELECT MAX(Kasus) FROM datakasus")
        kasus_terbesar = cur.fetchall()
        return kasus_terbesar

    def kasus_terkecil(self):
        cur = self.__db.cursor()
        cur.execute("SELECT MIN(Kasus) FROM datakasus")
        kasus_terkecil = cur.fetchall()
        return kasus_terkecil

    def read_jumlah_data(self):
        cur = self.__db.cursor()
        sql = "SELECT COUNT(Tanggal) AS JumlahData FROM datakasus"
        cur.execute(sql)
        jumlah_data = cur.fetchall()
        return jumlah_data

    def read_total_kasus(self):
        cur = self.__db.cursor()
        sql = "SELECT SUM(Kasus) AS JumlahKasus FROM datakasus"
        cur.execute(sql)
        total_kasus = cur.fetchall()
        return total_kasus

    # end for read

    # below are the search queries, it has the same sql as read but has the where clause
    def search_kasus(self, index):
        cur = self.__db.cursor()
        sql = "SELECT datakasus.Tanggal, datakasus.Kasus, datakasus.username, user.nama FROM datakasus INNER JOIN user ON datakasus.username=user.id WHERE Tanggal LIKE '%{0}%' OR nama LIKE '%{0}%' GROUP BY Tanggal ASC".format(index)
        cur.execute(sql)
        search_kasus = cur.fetchall()
        return search_kasus

    def search_user(self, index):
        cur = self.__db.cursor()
        sql = "SELECT id, nama, telepon, username, password, level, user_delete, " \
              "CASE WHEN user_delete IS NULL THEN 'User Aktif' ELSE 'User Tidak Aktif' " \
              "END AS StatusKaryawan " \
              "FROM user " \
              "WHERE id LIKE '{0}' " \
              "OR nama LIKE '%{0}%' " \
              "OR username LIKE '%{0}%' " \
              "OR telepon LIKE '%{0}%'" \
              "OR level LIKE '%{0}%'".format(index)
        cur.execute(sql)
        search_user = cur.fetchall()
        return search_user
    # end for search

    # below are update sql for kelola pengguna and kasus respectively
    def update(self, nama, username, password, telepon, level, id):
        cursor = self.__db.cursor()
        sql = "UPDATE user SET nama = '{0}', username = '{1}', password = '{2}', telepon = '{3}', level = '{4}' WHERE id = {5};".format(nama, username, password, telepon, level, id)
        cursor.execute(sql)
        self.__db.commit()

    def updateKasus(self, tanggal, kasus, username, userid):
        cursor = self.__db.cursor()
        sql = "UPDATE datakasus SET Tanggal = '{0}', Kasus = {1}, username = {2} WHERE id = {3}".format(tanggal, kasus, username, userid)
        cursor.execute(sql)
        self.__db.commit()
    # end for update

    # below are delete queries for both kelola pengguna and kasus respectively
    def delete(self, id):
        val = self.id = id
        cur = self.__db.cursor()
        sql = "DELETE FROM user WHERE id = %s"
        cur.execute(sql, (val,))
        self.__db.commit()

    def deletekasus(self, id):
        cur = self.__db.cursor()
        sql = "DELETE FROM datakasus WHERE id = {}".format(id)
        cur.execute(sql)
        self.__db.commit()

    # deactivate_user are used for kelola pengguna, in which it doesn't delete the user, but instead soft delete
    def deactivate_user(self, id):
        cur = self.__db.cursor()
        sql = "UPDATE user SET user_delete = now() WHERE id = {}".format(id)
        cur.execute(sql)
        self.__db.commit()

    # reactivate user
    def activate_user(self, id):
        cur = self.__db.cursor()
        sql = "UPDATE user SET user_delete = NULL WHERE id = {}".format(id)
        cur.execute(sql)
        self.__db.commit()

    # generate the necessary files for forecasting to work
    def GenerateCSVDataKasus(self):
        exported_path = Path('.').absolute() / 'exported' / 'Positif.csv'
        target = '%r'%str(exported_path)

        query = "SELECT 'Tanggal','Kasus' " \
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM datakasus " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ;".format(target)
        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateCSVDataPreVaksin(self):
        exported_path = Path('.').absolute() / 'exported' / 'DataPreVaksin.csv'
        target = '%r'%str(exported_path)

        query = "SELECT 'Tanggal','Kasus' "\
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM datakasus WHERE Tanggal >= '2020-04-07' AND Tanggal <= '2021-02-23' " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ".format(target)

        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateCSVDataPascaVaksin(self):
        exported_path = Path('.').absolute() / 'exported' / 'DataPascaVaksin.csv'
        target = '%r' % str(exported_path)

        query = "SELECT 'Tanggal','Kasus' "\
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM datakasus WHERE Tanggal >= '2021-02-24' " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ".format(target)
        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateCSVSmadaKraksaan(self):
        exported_path = Path('.').absolute() / 'exported' / 'smadakraksaan.csv'
        target = '%r' % str(exported_path)

        query = "SELECT 'Tanggal','Kasus' " \
                "UNION " \
                "SELECT DATE_FORMAT(tahun, '%d-%b-%Y'), " \
                "jumlah FROM smadakraksaan " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ;".format(target)

        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateAllData(self):
        dir = os.getcwd()
        target = dir + '\exported'
        try:
            self.GenerateCSVDataPreVaksin()
            self.GenerateCSVDataKasus()
            self.GenerateCSVDataPascaVaksin()
            self.GenerateCSVSmadaKraksaan()
        except mysql.connector.errors.DatabaseError:
            peringatan = messagebox.askquestion(title='Warning', message='File sudah ada, apakah Anda ingin hapus?')
            if peringatan == 'yes':
               filelist = glob.glob(os.path.join(target, "*.csv"))
               for f in filelist:
                   os.remove(f)
            else:
                pass
    # end for generate csv

    # this function is used to change password on the kelola pengguna
    def changePassword(self, password, id):
        cursor = self.__db.cursor()
        sql = "UPDATE user SET password = '{}' WHERE id = {}".format(password, id)
        cursor.execute(sql)
        self.__db.commit()

if __name__ == '__main__':
    Config()
    os.system('login.py')