import mysql.connector
import os, glob
import sys
import mysql.connector.locales.eng.client_error
from tkinter import messagebox
import ctypes
from pathlib import Path

class Config(object):

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

    def create(self, nama, telepon, role, username, password):
        self.nama = nama
        self.telepon = telepon
        self.username = username
        self.password = password
        self.role = role
        cursor = self.__db.cursor(buffered=True)
        results = cursor.execute("BEGIN;"
                       "INSERT INTO user (nama, telepon, role) "
                       "VALUES('{}', '{}', '{}');"
                       "INSERT INTO login (id_user, username, password) "
                       "VALUES(LAST_INSERT_ID(), '{}', '{}');"
                       .format(nama, telepon, role, username, password), multi=True)
        for cur in results:
            if cur.with_rows:
                cur.fetchall()
        self.__db.commit()

    def insertKasus(self, tanggal, jumlah):
        self.tanggal = tanggal
        self.jumlah = jumlah
        cursor = self.__db.cursor()
        value = (tanggal, jumlah)
        cursor.execute("INSERT INTO datareal (Tanggal, Kasus) VALUES (%s, %s)", value)
        self.__db.commit()


    def read_login(self):
        cur = self.__db.cursor()
        cur.execute("SELECT username FROM login")
        data_user = cur.fetchall()
        return data_user

    def read_kasus(self):
        cur = self.__db.cursor()
        cur.execute("SELECT Tanggal, Kasus, username FROM datareal")
        data_kasus = cur.fetchall()
        return data_kasus

    def read_user(self):
        cur = self.__db.cursor()
        cur.execute("SELECT user.id, user.nama, user.telepon, login.username, login.password, user.role "
                    "FROM user "
                    "INNER JOIN login ON user.id=login.id_user")
        data_user = cur.fetchall()
        return data_user

    def update(self, nama, telepon, role, username, password, id):
        cursor = self.__db.cursor(buffered=True)
        val = (nama, telepon, role, username, password, id)
        sql = "BEGIN;" \
              "UPDATE user SET nama = '{0}', telepon = '{1}', role= '{2}' WHERE id = {3};" \
              "UPDATE login SET username = '{4}', password = '{5}' WHERE id_user = {3};".format(nama, telepon, role, id, username, password)
        results = cursor.execute(sql, multi=True)
        for cur in results:
            if cur.with_rows:
                cur.fetchall()
        self.__db.commit()

    def delete(self, id):
        val = self.id = id
        cur = self.__db.cursor()
        sql = "DELETE FROM user WHERE id = %s"
        cur.execute(sql, (val,))
        self.__db.commit()

    def GenerateCSVDataReal(self):
        #export untuk datareal
        exported_path = Path('.').absolute() / 'exported' / 'Positif.csv'
        target = '%r'%str(exported_path)

        query = "SELECT 'Tanggal','Kasus' " \
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM datareal " \
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
                "Kasus FROM datareal WHERE Tanggal >= '2020-04-07' AND Tanggal <= '2021-02-23' " \
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
                "Kasus FROM datareal WHERE Tanggal >= '2021-02-24' AND Tanggal <= '2021-05-08' " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ".format(target)
        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateAllData(self):
        dir = os.getcwd()
        target = dir + '\exported'
        try:
            self.GenerateCSVDataPreVaksin()
            self.GenerateCSVDataReal()
            self.GenerateCSVDataPascaVaksin()
        except mysql.connector.errors.DatabaseError:
            peringatan = messagebox.askquestion(title='Warning', message='File sudah ada, apakah Anda ingin hapus?')
            if peringatan == 'yes':
               filelist = glob.glob(os.path.join(target, "*.csv"))
               for f in filelist:
                   os.remove(f)
            else:
                pass

    def changePassword(self, password, id):
        cursor = self.__db.cursor()
        sql = "UPDATE login SET password = '{}' WHERE id_user = {}".format(password, id)
        cursor.execute(sql)
        self.__db.commit()

if __name__ == '__main__':
    Config()
    os.system('login.py')