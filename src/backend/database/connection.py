from datetime import datetime

class CatatanPerkembangan:
    def __init__(self, id=None, tanaman_id=None, judul_catatan="", tanggal_perkembangan=None, tinggi=0, kondisi="", catatan=""):
        self.__id = id  # ID catatan
        self.__tanaman_id = tanaman_id  # ID tanaman yang terkait
        self.__judul_catatan = judul_catatan  # Judul catatan perkembangan
        self.__tanggal_perkembangan = tanggal_perkembangan if tanggal_perkembangan else datetime.now()  # Tanggal catatan
        self.__tinggi = tinggi  # Tinggi tanaman
        self.__kondisi = kondisi  # Kondisi tanaman (misal: sehat, layu, dsb.)
        self.__catatan = catatan  # Catatan tambahan

    def getCatatan(self):
        """Mengambil data sebuah catatan perkembangan"""
        return {
            'id': self.__id,
            'tanaman_id': self.__tanaman_id,
            'judul_catatan': self.__judul_catatan,
            'tanggal_perkembangan': self.__tanggal_perkembangan,
            'tinggi': self.__tinggi,
            'kondisi': self.__kondisi,
            'catatan': self.__catatan
        }

    def setCatatan(self, tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan):
        """Menyimpan data catatan baru"""
        self.__tanaman_id = tanaman_id
        self.__judul_catatan = judul_catatan
        self.__tanggal_perkembangan = tanggal_perkembangan
        self.__tinggi = tinggi
        self.__kondisi = kondisi
        self.__catatan = catatan

    def detailCatatan(self):
        """Menampilkan detail catatan perkembangan"""
        return self.getCatatan()

    def tampilkanInfo(self):
        """Menampilkan informasi catatan perkembangan"""
        return (
            f"Catatan '{self.__judul_catatan}' untuk tanaman ID {self.__tanaman_id}:\n"
            f"- Tanggal Perkembangan: {self.__tanggal_perkembangan}\n"
            f"- Tinggi: {self.__tinggi} cm\n"
            f"- Kondisi: {self.__kondisi}\n"
            f"- Catatan: {self.__catatan}"
        )
