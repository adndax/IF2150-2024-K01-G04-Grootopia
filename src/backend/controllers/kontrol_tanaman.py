# src/backend/controllers/kontrol_tanaman.py
from datetime import datetime
import sqlite3

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

    def getDaftarTanaman(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM tanaman")
        rows = cursor.fetchall()
        return [{'id': row[0], 
                'nama': row[1], 
                'waktu_tanam': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')} 
                for row in rows]

    def validasiInput(self, nama, waktu_tanam):
        return bool(nama and waktu_tanam)

    def prosesTambahTanaman(self, nama, waktu_tanam):
        if self.validasiInput(nama, waktu_tanam):
            try:
                cursor = self.__conn.cursor()
                cursor.execute(
                    "INSERT INTO tanaman (nama, waktu_tanam) VALUES (?, ?)",
                    (nama, waktu_tanam.strftime('%Y-%m-%d %H:%M:%S'))
                )
                self.__conn.commit()
                return True
            except sqlite3.Error:
                return False
        return False

    def prosesUpdateTanaman(self, id, nama, waktu_tanam):
        if self.validasiInput(nama, waktu_tanam):
            try:
                cursor = self.__conn.cursor()
                cursor.execute(
                    "UPDATE tanaman SET nama = ?, waktu_tanam = ? WHERE id = ?",
                    (nama, waktu_tanam.strftime('%Y-%m-%d %H:%M:%S'), id)
                )
                self.__conn.commit()
                return True
            except sqlite3.Error:
                return False
        return False

    def prosesHapusTanaman(self, id):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("DELETE FROM tanaman WHERE id = ?", (id,))
            self.__conn.commit()
            return True
        except sqlite3.Error:
            return False