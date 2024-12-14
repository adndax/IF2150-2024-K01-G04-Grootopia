import sqlite3
from datetime import datetime
from ..entity.jadwalPerawatan import JadwalPerawatan

class KontrolJadwal:
    def __init__(self, db_path='grootopia.db'):
        self.__db_path = db_path
        self.__conn = self.__createConnection()

    def __createConnection(self):
        try:
            conn = sqlite3.connect(self.__db_path)
            conn.execute('PRAGMA foreign_keys = ON;')
            self.__createTables(conn)
            return conn
        except sqlite3.Error as e:
            print(f"Database Connection Error: {e}")
            return None

    def __createTables(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jadwal_perawatan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deskripsi TEXT NOT NULL,
                    waktu DATETIME NOT NULL,
                    tanaman_id INTEGER NOT NULL,
                    FOREIGN KEY (tanaman_id) REFERENCES tanaman(id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Table Creation Error: {e}")

    def getDaftarJadwal(self):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("""
                SELECT j.id, j.deskripsi, j.waktu, j.tanaman_id, t.nama 
                FROM jadwal_perawatan j
                JOIN tanaman t ON j.tanaman_id = t.id
                ORDER BY j.waktu DESC
            """)
            rows = cursor.fetchall()
            
            daftar_jadwal = []
            for row in rows:
                jadwal_info = {
                    'id': row[0],
                    'deskripsi': row[1],
                    'waktu': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                    'tanaman_id': row[3],
                    'nama_tanaman': row[4]
                }
                daftar_jadwal.append(jadwal_info)
            
            return daftar_jadwal
        except sqlite3.Error as e:
            print(f"Error saat mengambil daftar jadwal: {e}")
            return []

    def tambahJadwal(self, deskripsi, waktu, tanaman_id):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "INSERT INTO jadwal_perawatan (deskripsi, waktu, tanaman_id) VALUES (?, ?, ?)",
                (deskripsi, waktu.strftime('%Y-%m-%d %H:%M:%S'), tanaman_id)
            )
            self.__conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saat menambah jadwal: {e}")
            return False

    def updateJadwal(self, id_jadwal, deskripsi, waktu, tanaman_id):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(
                "UPDATE jadwal_perawatan SET deskripsi = ?, waktu = ?, tanaman_id = ? WHERE id = ?",
                (deskripsi, waktu.strftime('%Y-%m-%d %H:%M:%S'), tanaman_id, id_jadwal)
            )
            self.__conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saat memperbarui jadwal: {e}")
            return False

    def hapusJadwal(self, id_jadwal):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("DELETE FROM jadwal_perawatan WHERE id = ?", (id_jadwal,))
            self.__conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saat menghapus jadwal: {e}")
            return False

    def getTanamanById(self, tanaman_id):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("SELECT * FROM tanaman WHERE id = ?", (tanaman_id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'nama': row[1],
                'waktu_tanam': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            } if row else None
        except sqlite3.Error as e:
            print(f"Error saat mengambil tanaman: {e}")
            return None