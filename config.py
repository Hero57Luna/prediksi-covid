import mysql.connector

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

    def create(self, nama, username, password, role, departement):

        self.nama = nama
        self.username = username
        self.password = password
        self.role = role
        self.departement = departement
        cursor = self.__db.cursor()
        val = (nama, username, password, role, departement)
        cursor.execute("INSERT INTO user (nama, username, password, role, departement) VALUES (%s, %s, %s, %s, %s)", val)
        self.__db.commit()


    def read(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM user")
        data_user = cur.fetchall()
        return data_user

    def update(self, nama, username, role, departement, kode):
        # self.nama = nama
        # self.username = username
        # self.role = role
        # self.departement = departement

        cursor = self.__db.cursor()
        val = (nama, username, role, departement, kode)
        sql = "UPDATE user SET nama=%s, username=%s, role=%s, departement=%s WHERE id=%s"
        cursor.execute(sql,(val))
        self.__db.commit()

    def delete(self, id):
        self.__db
        val = self.id = id
        cur = self.__db.cursor()
        sql = "DELETE FROM user WHERE id = %s"
        cur.execute(sql, (val,))
        self.__db.commit()


    def autoIncrement(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sisfo-covid"
        )
        cur = db.cursor()
        cuv = db.cursor()
        sqlkode = "SELECT max(id) FROM user"
        sql = "SELECT id FROM user"
        cur.execute(sqlkode)
        cuv.execute(sql)
        maxkode = cur.fetchone()

        if cuv.rowcount > 0:
            autohit = int(maxkode[0]) + 1
            hits = "000" + str(autohit)
            if len(hits) == 4:
                self.inputKode.insert(0, hits)
                self.inputNama.focus_set()
            elif len(hits) == 5:
                hit = "00" + str(autohit)
                self.inputKode.insert(0, hit)
                self.inputNama.focus_set()
            elif len(hits) == 6:
                hit = "0" + str(autohit)
                self.inputKode.insert(0, hit)
                self.inputNama.focus_set()
            elif len(hits) == 7:
                hit = "" + str(autohit)
                self.inputKode.insert(0, hit)
                self.inputNama.focus_set()
        else:
            hit = "0001"
            self.inputKode.insert(0, hit)
            self.inputNama.focus_set()