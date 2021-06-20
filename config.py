import mysql.connector
import os, glob, shutil
from tkinter import messagebox
from pathlib import Path

class Config(object):

    def __init__(self):
        self.__host = "localhost"
        self.__username = "root"
        self.__password = ""
        self.__database = "sisfo-covid"
        self.buatKoneksi()

    def buatKoneksi(self):
        db = mysql.connector.connect(
            host = self.__host,
            user = self.__username,
            password = self.__password,
            database = self.__database
        )
        try:
            self.__db = db
        except ConnectionRefusedError:
            print("Sambungan gagal")

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

    def create(self, nama, username, password, bagian):
        self.nama = nama
        self.username = username
        self.password = password
        self.bagian = bagian
        cursor = self.__db.cursor()
        val = (nama, username, password, bagian)
        cursor.execute("INSERT INTO user (nama, username, password, bagian) VALUES (%s, %s, %s, %s)", val)
        self.__db.commit()

    def insertKasus(self, tanggal, jumlah):
        self.tanggal = tanggal
        self.jumlah = jumlah
        cursor = self.__db.cursor()
        value = (tanggal, jumlah)
        cursor.execute("INSERT INTO kasus_probolinggo (Tanggal, Kasus) VALUES (%s, %s)", value)
        self.__db.commit()


    def read(self):
        cur = self.__db.cursor()
        cur.execute("SELECT id, nama, username, password, bagian FROM user")
        data_user = cur.fetchall()
        return data_user

    def update(self, nama, username, password, bagian, kode):
        cursor = self.__db.cursor()
        val = (nama, username, password, bagian, kode)
        sql = "UPDATE user SET nama=%s, username=%s, password=%s, bagian=%s WHERE id=%s"
        cursor.execute(sql,(val))
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

        #export untuk data pre vaksin
        exported_path_prevaksin = Path('.').absolute() / 'exported' / 'DataPreVaksin.csv'
        target_prevaksin = '%r'%str(exported_path_prevaksin)

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

        query = "SELECT 'Tanggal','Kasus' " \
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM dataprevaksin " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ;".format(target)
        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateCSVDataPascaVaksin(self):
        exported_path = Path('.').absolute() / 'exported' / 'DataPascaVaksin.csv'
        target = '%r' % str(exported_path)

        query = "SELECT 'Tanggal','Kasus' " \
                "UNION " \
                "SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), " \
                "Kasus FROM datapascavaksin " \
                "INTO OUTFILE {} " \
                "FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n' ;".format(target)
        cur = self.__db.cursor()
        cur.execute(query)

    def GenerateAllData(self):
        dir = os.getcwd()
        target = dir + '\exported'
        try:
            self.GenerateCSVDataReal()
            self.GenerateCSVDataPreVaksin()
            self.GenerateCSVDataPascaVaksin()
        except mysql.connector.errors.DatabaseError:
            peringatan = messagebox.askquestion(title='Warning', message='File sudah ada, apakah Anda ingin hapus?')
            if peringatan == 'yes':
               filelist = glob.glob(os.path.join(target, "*.csv"))
               for f in filelist:
                   os.remove(f)
            else:
                pass

if __name__ == '__main__':
    Config()
    os.system('python login.py')