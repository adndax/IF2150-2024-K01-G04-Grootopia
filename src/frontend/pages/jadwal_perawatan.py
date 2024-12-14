from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QDialog, QLineEdit, QDateTimeEdit, QHBoxLayout,
                             QScrollArea, QComboBox, QApplication)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QIcon
import os

from src.backend.controllers.kontrol_jadwal import KontrolJadwal
from src.backend.controllers.kontrol_tanaman import KontrolTanaman

class FormInputJadwal(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None, kontrol_tanaman=None):
        super().__init__(parent)
        self.__kontrol_tanaman = kontrol_tanaman
        self.daftar_tanaman = self.__kontrol_tanaman.getDaftarTanaman()
        
        self.setWindowTitle("Tambah Jadwal Perawatan" if not is_edit else "Sunting Jadwal Perawatan")
        self.setFixedSize(800, 700)
        self.setStyleSheet(""" QDialog { 
                           background-color: #DDE3D8; 
                           border-radius: 10px; 
                           color: #6C4530;
                        } 
                    """)
        
        self.setup_ui(is_edit, data)

    def setup_ui(self, is_edit, data):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel(self.windowTitle())
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Inter", 18, QFont.Bold))
        title.setStyleSheet("color: #3D2929")
        layout.addWidget(title)

        # Deskripsi Perawatan
        nama_label = QLabel("Deskripsi Tanaman")
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        nama_label.setStyleSheet("color: #3D2929")
        layout.addWidget(nama_label)

        self.deskripsi_input = QLineEdit()
        self.deskripsi_input.setPlaceholderText("Masukkan deskripsi perawatan")
        self.deskripsi_input.setFont(QFont("Inter", 12))
        self.deskripsi_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.deskripsi_input)

        # Waktu Perawatan
        waktu_label = QLabel("Waktu Perawatan")
        waktu_label.setFont(QFont("Inter", 12, QFont.Bold))
        waktu_label.setStyleSheet("color: #3D2929")
        layout.addWidget(waktu_label)

        waktu_container = QHBoxLayout()
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setFont(QFont("Inter", 12))
        self.datetime_edit.setStyleSheet("""
            QDateTimeEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #6C4530;
            }
            QDateTimeEdit::up-button, QDateTimeEdit::down-button {
                width: 20px; 
            }                      
        """)
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")

        waktu_container.addWidget(self.datetime_edit)
        layout.addWidget(self.datetime_edit)
        
        # Dropdown untuk memilih Tanaman
        tanaman_label = QLabel("Pilih Tanaman")
        tanaman_label.setFont(QFont("Inter", 12, QFont.Bold))
        tanaman_label.setStyleSheet("color: #3D2929")
        layout.addWidget(tanaman_label)

        self.tanaman_combo = QComboBox()
        self.tanaman_combo.setFont(QFont("Inter", 12))
        self.tanaman_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)

        layout.addWidget(self.tanaman_combo)

        # Tambahkan dropdown untuk Jenis Perawatan
        jenis_label = QLabel("Jenis Perawatan")
        jenis_label.setFont(QFont("Inter", 12, QFont.Bold))
        jenis_label.setStyleSheet("color: #3D2929")
        layout.addWidget(jenis_label)

        self.jenis_perawatan_combo = QComboBox()
        self.jenis_perawatan_combo.setFont(QFont("Inter", 12))
        self.jenis_perawatan_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        self.jenis_perawatan_combo.addItems(["Pemupukan", "Penyiraman"])
        layout.addWidget(self.jenis_perawatan_combo)

        # Tambahkan dropdown untuk Perulangan Perawatan
        perulangan_label = QLabel("Perulangan Perawatan")
        perulangan_label.setFont(QFont("Inter", 12, QFont.Bold))
        perulangan_label.setStyleSheet("color: #3D2929")
        layout.addWidget(perulangan_label)

        self.perulangan_perawatan_combo = QComboBox()
        self.perulangan_perawatan_combo.setFont(QFont("Inter", 12))
        self.perulangan_perawatan_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        self.perulangan_perawatan_combo.addItems(["Harian", "Mingguan", "Bulanan"])
        layout.addWidget(self.perulangan_perawatan_combo)

        # Handle saat mode edit
        if is_edit and data:
            # Atur nilai dropdown jenis perawatan dan perulangan
            self.jenis_perawatan_combo.setCurrentText(data.get('jenis_perawatan', ""))
            self.perulangan_perawatan_combo.setCurrentText(data.get('perulangan_perawatan', ""))

        # Tambahkan tanaman ke dalam combo box
        if(is_edit==0):
            for tanaman in self.daftar_tanaman:
                # Masukkan nama tanaman ke dropdown, simpan ID sebagai data
                self.tanaman_combo.addItem(tanaman['nama'], tanaman['id'])
        else :
            for tanaman in self.daftar_tanaman:
                # Masukkan nama tanaman ke dropdown, simpan ID sebagai data
                if(data['tanaman_id']==tanaman['id']):
                    self.tanaman_combo.addItem(tanaman['nama'], tanaman['id'])

        if is_edit and data:
            self.deskripsi_input.setText(data.get('deskripsi', ''))
            self.datetime_edit.setDateTime(data['waktu'])
            selected_tanaman_id = data.get('tanaman_id')
            index = self.tanaman_combo.findData(selected_tanaman_id)
            if index >= 0:
                self.tanaman_combo.setCurrentIndex(index)

        layout.addStretch()

        # Tombol Batal dan Simpan
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        batal_btn = QPushButton("BATAL")
        batal_btn.setFixedSize(150, 45)
        batal_btn.setFont(QFont("Inter", 12, QFont.Bold))
        batal_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333333;
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        batal_btn.clicked.connect(self.reject)

        simpan_btn = QPushButton("SIMPAN")
        simpan_btn.setFixedSize(150, 45)
        simpan_btn.setFont(QFont("Inter", 12, QFont.Bold))
        simpan_btn.setStyleSheet("""
            QPushButton {
                background-color: #59694D;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)
        simpan_btn.clicked.connect(self.accept)

        button_layout.addWidget(batal_btn)
        button_layout.addWidget(simpan_btn)
        button_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(button_layout)

class DeleteConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Konfirmasi")
        self.setFixedSize(400, 450)
        self.setStyleSheet("background-color: #DDE3D8;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 35, 30, 35)
        
        # Title
        title = QLabel("KONFIRMASI")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setStyleSheet("color: #3D2929")
        layout.addWidget(title)
        
        # Icon container
        icon_container = QWidget()
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 20, 0, 20)
        
        icon_label = QLabel()
        icon_path = os.path.join("img", "delete.svg")
        if os.path.exists(icon_path):
            icon_pixmap = QIcon(icon_path).pixmap(150, 150)
            icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_container)

        # Confirmation text
        confirm_text = QLabel("Apakah anda yakin ingin\nmenghapus Jadwal Perawatan ini?")
        confirm_text.setAlignment(Qt.AlignCenter)
        confirm_text.setFont(QFont("Inter", 14, QFont.Bold))
        confirm_text.setStyleSheet("color: #3D2929")
        layout.addWidget(confirm_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        batal_btn = QPushButton("BATAL")
        batal_btn.setFixedSize(135, 35)
        batal_btn.setFont(QFont("Inter", 12, QFont.Bold))
        batal_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333333;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        batal_btn.clicked.connect(self.reject)
        
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(135, 35)
        hapus_btn.setFont(QFont("Inter", 12, QFont.Bold))
        hapus_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B2C2C;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8b1c1c;
            }
        """)
        hapus_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(batal_btn)
        button_layout.addWidget(hapus_btn)
        button_layout.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(button_layout)

class JadwalUI(QWidget):
    def __init__(self):
        super().__init__()
        self.__kontrol_jadwal = KontrolJadwal()
        self.__kontrol_tanaman = KontrolTanaman()

        # Main layout
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        # Header layout
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 30, 30, 10)

        # Judul "Jadwal Perawatan"
        title_label = QLabel("Jadwal Perawatan")
        title_label.setFont(QFont("Inter", 30, QFont.Bold))
        title_label.setStyleSheet("color: #59694D;")
        title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(title_label)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari jadwal perawatan...")
        self.search_bar.setFont(QFont("Inter", 12))
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
                font-size: 14px;
                color: #6C4530;
                margin-bottom: 5;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_jadwal)
        header_layout.addWidget(self.search_bar)

        # Tambah jadwal button
        tambah_btn = QPushButton("+ Buat Jadwal Baru")
        tambah_btn.setFixedHeight(50)  # Atur tinggi tombol
        tambah_btn.setFont(QFont("Inter", 12, QFont.Bold))
        tambah_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6C4530;
                border: none;
                border-radius: 10px;
                padding: 15px 25px;
                text-align: center;
                font-weight: bold;
                border: 1px solid #E0E0E0;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        tambah_btn.clicked.connect(self.tampilkanKonfirmasiPenambahan)
        header_layout.addWidget(tambah_btn)

        self.__main_layout.addWidget(header_widget)

        # Scroll area untuk daftar jadwal
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background:  #EBF1E6;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #59694D;
                border-radius: 5px;
            }
        """)

        # Container untuk item-item jadwal
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.setContentsMargins(30, 15, 30, 30)
        scroll.setWidget(self.scroll_content)

        self.__main_layout.addWidget(scroll)

        # Load jadwal
        self.kelolaJadwal()

    def kelolaJadwal(self):
        self.__jadwal_list = self.__kontrol_jadwal.getDaftarJadwal()
        self.filtered_list = self.__jadwal_list
        self.perbaruiTampilan()

    def filter_jadwal(self, query):
        """Memfilter jadwal berdasarkan query pencarian"""
        query = query.lower()
        self.filtered_list = [jadwal for jadwal in self.__jadwal_list if query in jadwal['deskripsi'].lower()]
        self.perbaruiTampilan()

    def jadwal_item(self, jadwal):
        """Membuat item jadwal dengan nama, tombol sunting/hapus, dan dropdown untuk detail"""
        item_widget = QWidget()
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)
        main_layout = QVBoxLayout(item_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Tombol Dropdown
        dropdown_btn = QPushButton("▼")
        dropdown_btn.setFixedSize(30, 30)
        dropdown_btn.setStyleSheet("""
            QPushButton {
                background-color: #59694D; /* Warna hijau tua */
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)

        # Label deskripsi jadwal
        deskripsi_label = QLabel(f"{jadwal['deskripsi']}")
        deskripsi_label.setFont(QFont("Inter", 12, QFont.Bold))
        deskripsi_label.setStyleSheet("color: #6C4530; border: none;")
        deskripsi_label.setWordWrap(True)

        # Tombol Sunting
        sunting_btn = QPushButton("SUNTING")
        sunting_btn.setFixedSize(100, 30)
        sunting_btn.setFont(QFont("Inter", 12, QFont.Bold))
        sunting_btn.setStyleSheet("""
            QPushButton {
                background-color: #59694D;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)
        sunting_btn.clicked.connect(lambda: self.tampilkanKonfirmasiPenyuntingan(is_edit=True, jadwal=jadwal))

        # Tombol Hapus
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(100, 30)
        hapus_btn.setFont(QFont("Inter", 12, QFont.Bold))
        hapus_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B2C2C;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8b1c1c;
            }
        """)
        hapus_btn.clicked.connect(lambda: self.tampilkanKonfirmasiPenghapusan(jadwal))

        header_layout.addWidget(dropdown_btn)
        header_layout.addWidget(deskripsi_label)
        header_layout.addStretch()
        header_layout.addWidget(sunting_btn)
        header_layout.addWidget(hapus_btn)

        # Deskripsi Layout (Hidden by Default)
        deskripsi_widget = QWidget()
        deskripsi_widget.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        deskripsi_layout = QVBoxLayout(deskripsi_widget)
        deskripsi_layout.setSpacing(5)
        deskripsi_layout.setContentsMargins(10, 10, 10, 10)

        # Informasi Detail
        nama_info = QLabel(f"Nama Tanaman: {jadwal['nama_tanaman']}")
        nama_info.setFont(QFont("Inter", 12, QFont.Bold))
        nama_info.setStyleSheet("color: #59694D; border: none;")

        waktu_info = QLabel(f"Waktu Perawatan: {jadwal.get('waktu', 'Tidak tersedia')}")
        waktu_info.setFont(QFont("Inter", 12))
        waktu_info.setStyleSheet("color: #59694D; border: none;")

        # Informasi Jenis Perawatan
        jenis_info = QLabel(f"Jenis Perawatan: {jadwal.get('jenis_perawatan', 'Tidak tersedia')}")
        jenis_info.setFont(QFont("Inter", 12))
        jenis_info.setStyleSheet("color: #59694D; border: none;")

        # Informasi Perulangan Perawatan
        perulangan_info = QLabel(f"Perulangan: {jadwal.get('perulangan_perawatan', 'Tidak tersedia')}")
        perulangan_info.setFont(QFont("Inter", 12))
        perulangan_info.setStyleSheet("color: #59694D; border: none;")

        # Tambahkan informasi ke deskripsi layout
        deskripsi_layout.addWidget(nama_info)
        deskripsi_layout.addWidget(waktu_info)
        deskripsi_layout.addWidget(jenis_info)
        deskripsi_layout.addWidget(perulangan_info)

        # Default: Sembunyikan deskripsi
        deskripsi_widget.setVisible(False)

        # Tambahkan ke layout utama
        main_layout.addLayout(header_layout)
        main_layout.addWidget(deskripsi_widget)

        # Fungsi toggle dropdown
        def toggle_dropdown():
            is_visible = deskripsi_widget.isVisible()
            deskripsi_widget.setVisible(not is_visible)
            dropdown_btn.setText("▲" if not is_visible else "▼")

        dropdown_btn.clicked.connect(toggle_dropdown)

        # Tambahkan item widget ke scroll layout
        self.scroll_layout.addWidget(item_widget)

    def perbaruiTampilan(self):
        """Memperbarui tampilan setelah perubahan data"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for jadwal in self.filtered_list:
            self.jadwal_item(jadwal)

        self.scroll_layout.addStretch()

    def tampilkanKonfirmasiPenghapusan(self, jadwal):
        """Menampilkan dialog konfirmasi sebelum penghapusan"""
        dialog = DeleteConfirmDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            sukses = self.__kontrol_jadwal.hapusJadwal(jadwal['id'])
            self.tampilkanHasilOperasi(sukses, "Jadwal berhasil dihapus!", "Gagal menghapus jadwal!")
            if sukses:
                self.kelolaJadwal()

    def tampilkanKonfirmasiPenyuntingan(self, is_edit=False, jadwal=None):
        """Menampilkan dialog penyuntingan jadwal dengan konfirmasi"""
        form = FormInputJadwal(self, is_edit=is_edit, data=jadwal, kontrol_tanaman=self.__kontrol_tanaman)
        if form.exec_() == QDialog.Accepted:
            deskripsi = form.deskripsi_input.text()
            waktu = form.datetime_edit.dateTime().toPyDateTime()
            tanaman_id = form.tanaman_combo.currentData()
            jenis_perawatan = form.jenis_perawatan_combo.currentText()
            perulangan_perawatan = form.perulangan_perawatan_combo.currentText()

            if is_edit:
                sukses = self.__kontrol_jadwal.updateJadwal(jadwal['id'], deskripsi, waktu, tanaman_id, jenis_perawatan=jenis_perawatan, perulangan_perawatan=perulangan_perawatan)
                self.tampilkanHasilOperasi(sukses, "Jadwal berhasil disunting!", "Gagal menyunting jadwal!")
            else:
                sukses = self.__kontrol_jadwal.tambahJadwal(deskripsi, waktu, tanaman_id, jenis_perawatan=jenis_perawatan, perulangan_perawatan=perulangan_perawatan)
                self.tampilkanHasilOperasi(sukses, "Jadwal berhasil ditambahkan!", "Gagal menambahkan jadwal!")
            if sukses:
                self.kelolaJadwal()

    def tampilkanHasilOperasi(self, sukses, pesan_sukses, pesan_gagal):
        """Menampilkan dialog hasil operasi"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Sukses" if sukses else "Gagal")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("background-color: #DDE3D8;")
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 35, 30, 35)
        
        title = QLabel("SUKSES" if sukses else "GAGAL")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setStyleSheet("color: #3D2929")
        layout.addWidget(title)
        
        text = QLabel(pesan_sukses if sukses else pesan_gagal)
        text.setAlignment(Qt.AlignCenter)
        text.setFont(QFont("Inter", 14, QFont.Bold))
        text.setStyleSheet("color: #3D2929")
        layout.addWidget(text)
        
        ok_btn = QPushButton("OK")
        ok_btn.setFixedSize(135, 35)
        ok_btn.setFont(QFont("Inter", 12, QFont.Bold))
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333333;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        ok_btn.clicked.connect(dialog.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ok_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(btn_layout)
        
        dialog.exec_()

    def tampilkanKonfirmasiPenambahan(self):
        """Menampilkan dialog konfirmasi sebelum menambahkan jadwal"""
        self.tampilkanKonfirmasiPenyuntingan(is_edit=False)