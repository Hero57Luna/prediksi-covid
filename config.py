import mysql.connector
import os

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
        self.__db = db

    def koneksiDB(self):
        konek = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "sisfo-covid"
        }

        try:
            c = mysql.connector.connect(**konek)
            return c
        except:
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
        cursor.execute("INSERT INTO kasus (tanggal, kasus) VALUES (%s, %s)", value)
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

    def GenerateCSV(self):
        cwd = os.getcwd()
        dir = 'D:'
        namaFile = "\Positif.csv"
        query = "(SELECT 'Tanggal','Kasus') UNION (SELECT DATE_FORMAT(Tanggal, '%d-%b-%Y'), Kasus FROM kasus INTO OUTFILE '{}{}' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n')".format(dir, namaFile)
        cur = self.__db.cursor()
        cur.execute(query)

if __name__ == '__main__':
    Config()
    os.system('python login.py')