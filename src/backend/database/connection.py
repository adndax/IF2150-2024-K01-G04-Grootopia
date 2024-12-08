from sqlite3 import Error, Connection
import sqlite3


def create_connection():
    """Membuat koneksi ke database SQLite"""
    try:
        conn = sqlite3.connect('grootopia.db')
        return conn
    except Error as e:
        print(e)
        return None

def init_db():
    """Inisialisasi database dan membuat tabel jika belum ada"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tanaman (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_tanaman TEXT NOT NULL,
                    waktu_tanam DATETIME NOT NULL
                )
            """)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

