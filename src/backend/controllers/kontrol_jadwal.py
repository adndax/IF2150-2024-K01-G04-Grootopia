import sqlite3
from datetime import datetime
from ..entity.jadwalPerawatan import JadwalPerawatan
from ..entity.tanaman import Tanaman
from PyQt5.QtCore import Qt, QDateTime

class KontrolJadwal:
    def __init__(self):
        self.__conn = self.__createConnection()

    def __createConnection(self):
        try:
            conn = sqlite3.connect('grootopia.db')
            self.__createTable(conn)
            return conn
        except sqlite3.Error as e:
            print(f"Error saat membuat koneksi: {e}")
            return None

    def __createTable(self, conn):
        query = '''
        CREATE TABLE IF NOT EXISTS jadwal_perawatan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            waktu DATETIME NOT NULL,
            tanaman_id INTEGER NOT NULL,
            FOREIGN KEY (tanaman_id) REFERENCES tanaman(id)
        )
        '''
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saat membuat tabel: {e}")

    def validasiInput(self, deskripsi, waktu):
        return bool(deskripsi and waktu)

    def getDaftarJadwal(self):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("SELECT * FROM jadwal_perawatan")
            rows = cursor.fetchall()
            
            daftar_jadwal = []
            for row in rows:
                jadwal = JadwalPerawatan(
                    id=row[0],
                    deskripsi=row[1],
                    waktu=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                    tanaman_id=row[3]
                )
                
                # Ambil nama tanaman berdasarkan tanaman_id
                tanaman = self.getTanamanById(jadwal.getJadwal()['tanaman_id'])
                nama_tanaman = tanaman['nama'] if tanaman else "Tanaman Tidak Dikenal"
                
                # Menyusun informasi untuk ditampilkan
                jadwal_info = {
                    'id':jadwal.getJadwal()['id'],
                    'deskripsi': jadwal.getJadwal()['deskripsi'],
                    'nama_tanaman': nama_tanaman,
                    'waktu': jadwal.getJadwal()['waktu']
                }
                daftar_jadwal.append(jadwal_info)
            
            return daftar_jadwal
        except sqlite3.Error as e:
            print(f"Error saat mengambil data: {e}")
            return []

    def getTanamanById(self, tanaman_id):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM tanaman WHERE id = ?", (tanaman_id,))
        row = cursor.fetchone() 
        if row:
            return Tanaman(
                id=row[0],
                nama=row[1],
                waktu_tanam=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            ).getTanaman()
        return None 

    def tambahJadwal(self, deskripsi, waktu, tanaman_id):
        if self.validasiInput(deskripsi, waktu):
            try:
                jadwal = JadwalPerawatan(id=id, deskripsi=deskripsi, waktu=waktu, tanaman_id=tanaman_id)
                waktu_jadwal = jadwal.getJadwal()['waktu'] 

                if isinstance(waktu_jadwal, QDateTime):
                    waktu_jadwal = waktu_jadwal.toPyDateTime()

                cursor = self.__conn.cursor()
                cursor.execute(
                    "INSERT INTO jadwal_perawatan (deskripsi, waktu, tanaman_id) VALUES (?, ?, ?)",
                    (jadwal.getJadwal()['deskripsi'],
                     jadwal.getJadwal()['waktu'].strftime('%Y-%m-%d %H:%M:%S'),
                     jadwal.getJadwal()['tanaman_id'])
                )
                self.__conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error saat menambah jadwal: {e}")
                return False
        return False

    def updateJadwal(self, id, deskripsi, waktu, tanaman_id):
        if self.validasiInput(deskripsi, waktu):
            try:
                jadwal = JadwalPerawatan(id=id, deskripsi=deskripsi, waktu=waktu, tanaman_id=tanaman_id)
                cursor = self.__conn.cursor()
                cursor.execute(
                    "UPDATE jadwal_perawatan SET deskripsi = ?, waktu = ?, tanaman_id = ? WHERE id = ?",
                    (jadwal.getJadwal()['deskripsi'],
                     jadwal.getJadwal()['waktu'].strftime('%Y-%m-%d %H:%M:%S'),
                     jadwal.getJadwal()['tanaman_id'],
                     jadwal.getJadwal()['id'])
                )
                self.__conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error saat memperbarui jadwal: {e}")
                return False
        return False

    def hapusJadwal(self, id):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("DELETE FROM jadwal_perawatan WHERE id = ?", (id,))
            self.__conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saat menghapus jadwal: {e}")
            return False
