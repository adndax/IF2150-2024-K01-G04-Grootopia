from datetime import datetime
import sqlite3
from ..entity.tanaman import Tanaman 

class KontrolTanaman:
    def __init__(self):
        self.__conn = self.__createConnection()
        
    def __createConnection(self):
        try:
            conn = sqlite3.connect('grootopia.db')
            self.__createTable(conn)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None
    
    def __createTable(self, conn):
        query = '''CREATE TABLE IF NOT EXISTS tanaman
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nama TEXT NOT NULL,
                   waktu_tanam DATETIME NOT NULL)'''
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(e)


    def validasiInput(self, nama, waktu_tanam):
        return bool(nama and waktu_tanam)


    def getDaftarTanaman(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM tanaman")
        rows = cursor.fetchall()
        return [Tanaman(
            id=row[0], 
            nama=row[1], 
            waktu_tanam=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        ).getTanaman() for row in rows]

    def prosesTambahTanaman(self, nama, waktu_tanam):
        if self.validasiInput(nama, waktu_tanam):
            try:
                tanaman = Tanaman(nama=nama, waktu_tanam=waktu_tanam)
                cursor = self.__conn.cursor()
                cursor.execute(
                    "INSERT INTO tanaman (nama, waktu_tanam) VALUES (?, ?)",
                    (tanaman.getTanaman()['nama'], 
                     tanaman.getTanaman()['waktu_tanam'].strftime('%Y-%m-%d %H:%M:%S'))
                )
                self.__conn.commit()
                return True
            except sqlite3.Error:
                return False
        return False

    def prosesUpdateTanaman(self, id, nama, waktu_tanam):
        if self.validasiInput(nama, waktu_tanam):
            try:
                tanaman = Tanaman(id=id, nama=nama, waktu_tanam=waktu_tanam)
                cursor = self.__conn.cursor()
                cursor.execute(
                    "UPDATE tanaman SET nama = ?, waktu_tanam = ? WHERE id = ?",
                    (tanaman.getTanaman()['nama'],
                     tanaman.getTanaman()['waktu_tanam'].strftime('%Y-%m-%d %H:%M:%S'),
                     tanaman.getTanaman()['id'])
                )
                self.__conn.commit()
                return True
            except sqlite3.Error:
                return False
        return False