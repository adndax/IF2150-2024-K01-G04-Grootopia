from datetime import datetime
import sqlite3
from ..entity.catatan import Catatan

class KontrolCatatanPerkembangan:
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
        query = '''
        CREATE TABLE IF NOT EXISTS catatan_perkembangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanaman_id INTEGER NOT NULL,
            judul_catatan TEXT NOT NULL,
            tanggal_perkembangan DATETIME NOT NULL,
            tinggi INTEGER NOT NULL,
            kondisi TEXT NOT NULL,
            catatan TEXT NOT NULL,
            FOREIGN KEY (tanaman_id) REFERENCES tanaman (id)
        )'''
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    def validasiInput(self, tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
        return bool(tanaman_id and judul_catatan and tanggal_perkembangan and tinggi and kondisi and catatan)

    def getDaftarCatatan(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM catatan_perkembangan")
        rows = cursor.fetchall()
        return [Catatan(
            id=row[0],
            tanaman_id=row[1],
            judul_catatan=row[2],
            tanggal_perkembangan=datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
            tinggi=row[4],
            kondisi=row[5],
            catatan=row[6]
        ).getCatatan() for row in rows]

    def prosesTambahCatatan(self, tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
        if self.validasiInput(tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
            try:
                catatan_perkembangan = Catatan(
                    tanaman_id=tanaman_id, 
                    judul_catatan=judul_catatan, 
                    tanggal_perkembangan=tanggal_perkembangan,
                    tinggi=tinggi, 
                    kondisi=kondisi, 
                    catatan=catatan
                )
                cursor = self.__conn.cursor()
                cursor.execute(
                    '''INSERT INTO catatan_perkembangan 
                    (tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (catatan_perkembangan.getCatatan()['tanaman_id'],
                     catatan_perkembangan.getCatatan()['judul_catatan'],
                     catatan_perkembangan.getCatatan()['tanggal_perkembangan'].strftime('%Y-%m-%d %H:%M:%S'),
                     catatan_perkembangan.getCatatan()['tinggi'],
                     catatan_perkembangan.getCatatan()['kondisi'],
                     catatan_perkembangan.getCatatan()['catatan'])
                )
                self.__conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error saat menambah catatan: {e}")
                return False
        return False

    def prosesUpdateCatatan(self, id, tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
        if self.validasiInput(tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
            try:
                catatan_perkembangan = Catatan(
                    id=id,
                    tanaman_id=tanaman_id, 
                    judul_catatan=judul_catatan, 
                    tanggal_perkembangan=tanggal_perkembangan,
                    tinggi=tinggi, 
                    kondisi=kondisi, 
                    catatan=catatan
                )
                cursor = self.__conn.cursor()
                cursor.execute(
                    '''UPDATE catatan_perkembangan
                       SET tanaman_id = ?, judul_catatan = ?, tanggal_perkembangan = ?, 
                           tinggi = ?, kondisi = ?, catatan = ?
                       WHERE id = ?''',
                    (catatan_perkembangan.getCatatan()['tanaman_id'],
                     catatan_perkembangan.getCatatan()['judul_catatan'],
                     catatan_perkembangan.getCatatan()['tanggal_perkembangan'].strftime('%Y-%m-%d %H:%M:%S'),
                     catatan_perkembangan.getCatatan()['tinggi'],
                     catatan_perkembangan.getCatatan()['kondisi'],
                     catatan_perkembangan.getCatatan()['catatan'],
                     catatan_perkembangan.getCatatan()['id'])
                )
                self.__conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error saat memperbarui catatan: {e}")
                return False
        return False

    def prosesHapusCatatan(self, id):
        """Memproses penghapusan catatan perkembangan"""
        try:
            cursor = self.__conn.cursor()
            cursor.execute("DELETE FROM catatan_perkembangan WHERE id = ?", (id,))
            self.__conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saat menghapus catatan: {e}")
            return False
