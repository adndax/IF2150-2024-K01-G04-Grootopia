# src/backend/models/tanaman.py
from datetime import datetime

class Tanaman:
    def __init__(self, id=None, nama="", waktu_tanam=None):
        self.__id = id  
        self.__nama = nama  
        self.__waktu_tanam = waktu_tanam if waktu_tanam else datetime.now()  

    def getTanaman(self):
        """Mengambil data sebuah tanaman"""
        return {
            'id': self.__id,
            'nama': self.__nama,
            'waktu_tanam': self.__waktu_tanam
        }

    def setTanaman(self, nama, waktu_tanam):
        """Menyimpan data tanaman baru"""
        self.__nama = nama
        self.__waktu_tanam = waktu_tanam

    def updateTanaman(self, nama, waktu_tanam):
        """Memperbarui data tanaman"""
        self.__nama = nama
        self.__waktu_tanam = waktu_tanam

    def detailTanaman(self):
        """Menampilkan detail satu tanaman"""
        return self.getTanaman()

    def tampilkanInfo(self):
        """Menampilkan informasi tanaman"""
        return f"Tanaman {self.__nama} ditanam pada {self.__waktu_tanam}"