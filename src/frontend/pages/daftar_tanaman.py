from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QDialog, QLineEdit, QCalendarWidget, QHBoxLayout,
                           QDateTimeEdit, QSizePolicy, QScrollArea)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QIcon
from src.backend.controllers.kontrol_tanaman import KontrolTanaman
import os

class FormInputTanaman(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Tanaman" if not is_edit else "Sunting Tanaman")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
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
        
        # Nama Tanaman
        nama_label = QLabel("Nama Tanaman")
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        nama_label.setStyleSheet("color: #3D2929")
        layout.addWidget(nama_label)
        
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Masukkan nama tanaman")
        self.nama_input.setFont(QFont("Inter", 12))
        self.nama_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.nama_input)
        
        # Waktu Tanam
        waktu_label = QLabel("Waktu Tanam")
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
        layout.addLayout(waktu_container)

        if is_edit and data:
            self.nama_input.setText(data.get('nama', ''))
            if 'waktu_tanam' in data:
                self.datetime_edit.setDateTime(data['waktu_tanam'])
        
        layout.addStretch()
        
        # Buttons
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
                border-radius: 10px;
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
                border-radius: 10px;
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
        confirm_text = QLabel("Apakah anda yakin ingin\nmenghapus tanaman ini?")
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

class TanamanUI(QWidget):
    def __init__(self):
        super().__init__()
        self.__kontrol_tanaman = KontrolTanaman()
        
        # Main layout untuk seluruh widget
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        # Container untuk tombol Tambah
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(30, 30, 30, 10)
        
        # Judul "Tanaman"
        title_label = QLabel("Tanaman")
        title_label.setFont(QFont("Inter", 30, QFont.Bold))
        title_label.setStyleSheet("color: #59694D;")
        title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(title_label)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari tanaman...")
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
        self.search_bar.textChanged.connect(self.filter_tanaman)
        header_layout.addWidget(self.search_bar)

        self.__main_layout.addWidget(self.header_widget)

        # Tambah Tanaman button
        tambah_btn = QPushButton("+ Tambah Tanaman")
        tambah_btn.setFixedHeight(50)
        tambah_btn.setFont(QFont("Inter", 12, QFont.Bold))
        tambah_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6C4530;
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
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
        
        self.__main_layout.addWidget(self.header_widget)
        
        # Scroll Area untuk daftar tanaman
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #EBF1E6;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #59694D;
                border-radius: 5px;
            }
        """)
        
        # Container untuk item-item tanaman
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.setContentsMargins(30, 15, 30, 30)
        scroll.setWidget(self.scroll_content)
        
        self.__main_layout.addWidget(scroll)
        
        self.kelolaTanaman()

    def kelolaTanaman(self):
        self.__tanaman_list = self.__kontrol_tanaman.getDaftarTanaman()
        self.filtered_list = self.__tanaman_list 
        self.perbaruiTampilan()

    def filter_tanaman(self, query):
        """Memfilter daftar tanaman berdasarkan query pencarian"""
        query = query.lower()
        self.filtered_list = [tanaman for tanaman in self.__tanaman_list if query in tanaman['nama'].lower()]
        self.perbaruiTampilan()

    def tanaman_item(self, tanaman):
        """Membuat item tanaman dengan tombol dropdown untuk deskripsi"""
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
                background-color: #F5F5F5;
            }
        """)
        
        # Nama Tanaman
        nama_label = QLabel(tanaman['nama'])
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        nama_label.setStyleSheet("color: #6C4530; border: none;")
        
        # Tombol Sunting
        sunting_btn = QPushButton("SUNTING")
        sunting_btn.setFixedSize(100, 30)
        sunting_btn.setStyleSheet("""
            QPushButton {
                background-color: #59694D;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)
        sunting_btn.clicked.connect(lambda: self.tampilkanKonfirmasiPenyuntingan(is_edit=True, tanaman=tanaman))

        # Tombol Hapus
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(100, 30)
        hapus_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B2C2C;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8b1c1c;
            }
        """)
        hapus_btn.clicked.connect(lambda: self.tampilkanKonfirmasiPenghapusan(tanaman))
        
        header_layout.addWidget(dropdown_btn)
        header_layout.addWidget(nama_label)
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

        # Informasi Deskripsi
        nama_info = QLabel(f"Nama Tanaman: {tanaman['nama']}")
        nama_info.setFont(QFont("Inter", 12, QFont.Bold))
        nama_info.setStyleSheet("color: #59694D; border: none;")

        waktu_info = QLabel(f"Waktu Tanam: {tanaman.get('waktu_tanam', 'Tidak tersedia')}")
        waktu_info.setFont(QFont("Inter", 12))
        waktu_info.setStyleSheet("color: #59694D; border: none;")

        deskripsi_layout.addWidget(nama_info)
        deskripsi_layout.addWidget(waktu_info)

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

        # Tambahkan item ke daftar
        self.scroll_layout.addWidget(item_widget)

    def perbaruiTampilan(self):
        """Memperbarui tampilan setelah perubahan data"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for tanaman in self.filtered_list:
            self.tanaman_item(tanaman)
        
        self.scroll_layout.addStretch()
            
    # Tambahkan fungsi untuk konfirmasi penghapusan di `CatatanPerkembangan`
    def hapus_catatan(self, id_catatan):
        dialog = DeleteConfirmDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            sukses = self.__kontrol_catatan.prosesHapusCatatan(id_catatan)
            self.tampilkanHasilOperasi(sukses, "Catatan berhasil dihapus!", "Gagal menghapus catatan!")
            if sukses:
                self.kelolaPerkembanganTanaman()

    # Tambahkan fungsi untuk menampilkan dialog hasil
    def tampilkanHasilOperasi(self, sukses, pesan_sukses, pesan_gagal):
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

    # Implementasi fungsi serupa pada TanamanUI
    def tampilkanKonfirmasiPenghapusan(self, tanaman):
        dialog = DeleteConfirmDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            sukses = self.__kontrol_tanaman.prosesHapusTanaman(tanaman['id'])
            self.tampilkanHasilOperasi(sukses, "Tanaman berhasil dihapus!", "Gagal menghapus tanaman!")
            if sukses:
                self.kelolaTanaman()
    
    def tampilkanKonfirmasiPenyuntingan(self, is_edit=False, tanaman=None):
        """Menampilkan form input dan konfirmasi sebelum menyimpan perubahan"""
        sukses = False
        dialog = FormInputTanaman(self, is_edit, tanaman)
        
        if dialog.exec_() == QDialog.Accepted:
            nama = dialog.nama_input.text()
            waktu_tanam = dialog.datetime_edit.dateTime().toPyDateTime()
        
            if is_edit:
                # Dialog konfirmasi penyuntingan
                confirm_dialog = QDialog(self)
                confirm_dialog.setWindowTitle("Konfirmasi Penyuntingan")
                confirm_dialog.setFixedSize(400, 250)
                confirm_dialog.setStyleSheet("background-color: #DDE3D8;")

                layout = QVBoxLayout(confirm_dialog)
                layout.setSpacing(20)
                layout.setContentsMargins(20, 20, 20, 20)

                # Title
                title = QLabel("KONFIRMASI")
                title.setAlignment(Qt.AlignCenter)
                title.setFont(QFont("Inter", 16, QFont.Bold))
                title.setStyleSheet("color: #3D2929")
                layout.addWidget(title)

                # Dynamic confirmation text
                text = QLabel(f"Apakah Anda yakin ingin\nmenyimpan perubahan untuk {tanaman['nama']}?")
                text.setAlignment(Qt.AlignCenter)
                text.setFont(QFont("Inter", 14, QFont.Bold))
                text.setStyleSheet("color: #3D2929")
                layout.addWidget(text)

                # Buttons
                button_layout = QHBoxLayout()
                batal_btn = QPushButton("BATAL")
                batal_btn.setFixedSize(120, 35)
                batal_btn.setFont(QFont("Inter", 12, QFont.Bold))
                batal_btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #333333;
                        border: none;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)
                batal_btn.clicked.connect(confirm_dialog.reject)

                simpan_btn = QPushButton("SIMPAN")
                simpan_btn.setFixedSize(120, 35)
                simpan_btn.setFont(QFont("Inter", 12, QFont.Bold))
                simpan_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #59694D;
                        color: white;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #4a5a3e;
                    }
                """)
                simpan_btn.clicked.connect(confirm_dialog.accept)

                button_layout.addWidget(batal_btn)
                button_layout.addWidget(simpan_btn)
                button_layout.setAlignment(Qt.AlignCenter)
                layout.addLayout(button_layout)

                # Show confirmation dialog
                if confirm_dialog.exec_() == QDialog.Accepted:
                    sukses = self.__kontrol_tanaman.prosesUpdateTanaman(tanaman['id'], nama, waktu_tanam)
                    self.tampilkanHasilOperasi(sukses, "Tanaman berhasil disunting!", "Gagal menyunting tanaman!")
            else:
                sukses = self.__kontrol_tanaman.prosesTambahTanaman(nama, waktu_tanam)
                self.tampilkanHasilOperasi(sukses, "Tanaman berhasil ditambahkan!", "Gagal menambahkan tanaman!")
            
            if sukses:
                self.kelolaTanaman()

    def tampilkanKonfirmasiPenambahan(self):
        """Menampilkan form input untuk menambahkan tanaman baru dengan konfirmasi"""
        dialog = FormInputTanaman(self, is_edit=False)
        
        if dialog.exec_() == QDialog.Accepted:
            # Ambil data dari form
            nama = dialog.nama_input.text()
            waktu_tanam = dialog.datetime_edit.dateTime().toPyDateTime()
            
            # Dialog konfirmasi sebelum menyimpan
            confirm_dialog = QDialog(self)
            confirm_dialog.setWindowTitle("Konfirmasi Penambahan")
            confirm_dialog.setFixedSize(400, 250)
            confirm_dialog.setStyleSheet("background-color: #DDE3D8;")
            
            layout = QVBoxLayout(confirm_dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            # Title
            title = QLabel("KONFIRMASI")
            title.setAlignment(Qt.AlignCenter)
            title.setFont(QFont("Inter", 16, QFont.Bold))
            title.setStyleSheet("color: #3D2929")
            layout.addWidget(title)

            # Confirmation text
            text = QLabel(f"Apakah Anda yakin ingin\nmenambahkan tanaman dengan nama {nama}?")
            text.setAlignment(Qt.AlignCenter)
            text.setFont(QFont("Inter", 14, QFont.Bold))
            text.setStyleSheet("color: #3D2929")
            layout.addWidget(text)

            # Buttons
            button_layout = QHBoxLayout()
            batal_btn = QPushButton("BATAL")
            batal_btn.setFixedSize(120, 35)
            batal_btn.setFont(QFont("Inter", 12, QFont.Bold))
            batal_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #333333;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            batal_btn.clicked.connect(confirm_dialog.reject)

            simpan_btn = QPushButton("TAMBAHKAN")
            simpan_btn.setFixedSize(120, 35)
            simpan_btn.setFont(QFont("Inter", 12, QFont.Bold))
            simpan_btn.setStyleSheet("""
                QPushButton {
                    background-color: #59694D;
                    color: white;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #4a5a3e;
                }
            """)
            simpan_btn.clicked.connect(confirm_dialog.accept)

            button_layout.addWidget(batal_btn)
            button_layout.addWidget(simpan_btn)
            button_layout.setAlignment(Qt.AlignCenter)
            layout.addLayout(button_layout)

            if confirm_dialog.exec_() == QDialog.Accepted:
                sukses = self.__kontrol_tanaman.prosesTambahTanaman(nama, waktu_tanam)
                self.tampilkanHasilOperasi(sukses, "Tanaman berhasil ditambahkan!", "Gagal menambahkan tanaman!")
                if sukses:
                    self.kelolaTanaman()