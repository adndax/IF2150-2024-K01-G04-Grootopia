from datetime import datetime

class JadwalPerawatan:
    def __init__(self, id=None, deskripsi="", waktu=None, tanaman_id=None):
        self.__id = id  # ID jadwal perawatan
        self.__deskripsi = deskripsi  # Deskripsi perawatan
        self.__waktu = waktu if waktu else datetime.now()  # Waktu perawatan
        self.__tanaman_id = tanaman_id  # ID tanaman yang dirawat

    def getJadwal(self):
        """Mengambil data jadwal perawatan"""
        return {
            'id': self.__id,
            'deskripsi': self.__deskripsi,
            'waktu': self.__waktu,
            'tanaman_id': self.__tanaman_id
        }

    def setJadwal(self, deskripsi, waktu, tanaman_id):
        """Menyimpan data jadwal perawatan baru"""
        self.__deskripsi = deskripsi
        self.__waktu = waktu
        self.__tanaman_id = tanaman_id

    def updateJadwal(self, deskripsi, waktu, tanaman_id):
        """Memperbarui data jadwal perawatan"""
        self.__deskripsi = deskripsi
        self.__waktu = waktu
        self.__tanaman_id = tanaman_id

    def detailJadwal(self):
        """Menampilkan detail jadwal perawatan"""
        return self.getJadwal()

    def tampilkanInfo(self):
        """Menampilkan informasi jadwal perawatan"""
        return f"Jadwal perawatan untuk tanaman ID {self.__tanaman_id} dengan deskripsi '{self.__deskripsi}' pada {self.__waktu}"
