from datetime import datetime

class JadwalPerawatan:
    def __init__(self, id=None, deskripsi="", waktu=None, tanaman_id=None, tanaman_nama=None):
        self.__id = id
        self.__deskripsi = deskripsi
        self.__waktu = waktu if waktu else datetime.now()
        self.__tanaman_id = tanaman_id
        self.__tanaman_nama = tanaman_nama  

    def getJadwal(self):
        return {
            'id': self.__id,
            'deskripsi': self.__deskripsi,
            'waktu': self.__waktu,
            'tanaman_id': self.__tanaman_id,
            'tanaman_nama': self.__tanaman_nama
        }

    def setJadwal(self, deskripsi, waktu, tanaman_id, tanaman_nama):
        self.__deskripsi = deskripsi
        self.__waktu = waktu
        self.__tanaman_id = tanaman_id
        self.__tanaman_nama = tanaman_nama