from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QDialog, QLineEdit, QDateTimeEdit, QHBoxLayout,
                             QScrollArea, QComboBox, QApplication)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

from src.backend.controllers.kontrol_jadwal import KontrolJadwal
from src.backend.controllers.kontrol_tanaman import KontrolTanaman

class FormInputJadwal(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None, kontrol_tanaman=None):
        super().__init__(parent)
        self.__kontrol_tanaman = kontrol_tanaman
        self.daftar_tanaman = self.__kontrol_tanaman.getDaftarTanaman()
        
        self.setWindowTitle("Tambah Jadwal Perawatan" if not is_edit else "Sunting Jadwal Perawatan")
        self.setFixedSize(800, 600)
        self.setStyleSheet(""" QDialog { background-color: #DDE3D8; border-radius: 20px; } """)
        
        self.setup_ui(is_edit, data)

    def setup_ui(self, is_edit, data):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Deskripsi input
        deskripsi_label = QLabel("Deskripsi Perawatan")
        deskripsi_label.setFont(QFont("Inter", 12, QFont.Bold))
        layout.addWidget(deskripsi_label)

        self.deskripsi_input = QLineEdit()
        self.deskripsi_input.setPlaceholderText("Masukkan deskripsi perawatan")
        self.deskripsi_input.setFont(QFont("Inter", 12))
        self.deskripsi_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 8px;
                min-height: 45px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.deskripsi_input)

        # Waktu Perawatan
        waktu_label = QLabel("Waktu Perawatan")
        waktu_label.setFont(QFont("Inter", 12, QFont.Bold))
        layout.addWidget(waktu_label)

        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setFont(QFont("Inter", 12))
        self.datetime_edit.setStyleSheet("""
            QDateTimeEdit {
                padding: 12px;
                background: white;
                border-radius: 8px;
                min-height: 45px;
                font-size: 14px;
            }
        """)
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        layout.addWidget(self.datetime_edit)

        # Dropdown untuk memilih Tanaman
        tanaman_label = QLabel("Pilih Tanaman")
        tanaman_label.setFont(QFont("Inter", 12, QFont.Bold))
        layout.addWidget(tanaman_label)

        self.tanaman_combo = QComboBox()
        self.tanaman_combo.setFont(QFont("Inter", 12))

        # Tambahkan tanaman ke dalam combo box
        for tanaman in self.daftar_tanaman:
            self.tanaman_combo.addItem(tanaman['nama'], tanaman['id']) 

        layout.addWidget(self.tanaman_combo)

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
        title.setFont(QFont("Inter", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Confirmation text
        confirm_text = QLabel("Apakah anda yakin ingin\nmenghapus Jadwal Perawatan ini?")
        confirm_text.setAlignment(Qt.AlignCenter)
        confirm_text.setFont(QFont("Inter", 12))
        layout.addWidget(confirm_text)
        
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
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        batal_btn.clicked.connect(self.reject)
        
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(150, 45)
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

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 30, 30, 15)

        # Tambah jadwal button
        tambah_btn = QPushButton("+ Buat Jadwal Baru")
        tambah_btn.setFixedHeight(70)
        tambah_btn.setFont(QFont("Inter", 12, QFont.Bold))
        tambah_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6C4530;
                border: none;
                border-radius: 16px;
                padding: 15px 25px;
                text-align: center;
                font-weight: bold;
                border: 1px solid #E0E0E0;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        tambah_btn.clicked.connect(self.tampilkanFormInput)
        header_layout.addWidget(tambah_btn)

        self.__main_layout.addWidget(header_widget)

        # Scroll Area untuk daftar jadwal
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #f1f1f1;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                border-radius: 5px;
            }
        """)

        # Container untuk item-item jadwal
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(25)
        self.scroll_layout.setContentsMargins(30, 15, 30, 30)
        scroll.setWidget(self.scroll_content)

        self.__main_layout.addWidget(scroll)

        self.kelolaJadwal()

    def kelolaJadwal(self):
        self.__jadwal_list = self.__kontrol_jadwal.getDaftarJadwal()
        self.daftar_tanaman = self.__kontrol_tanaman.getDaftarTanaman() 
        self.perbaruiTampilan()

    def jadwal_item(self, jadwal):
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(25, 20, 25, 20)
        item_layout.setSpacing(20)

        # Deskripsi label
        deskripsi_label = QLabel(f"{jadwal['nama_tanaman']} | {jadwal['deskripsi']} | {jadwal['waktu']}")
        deskripsi_label.setFont(QFont("Inter", 12, QFont.Bold))
        deskripsi_label.setStyleSheet("color: #6C4530; border: none;")
        deskripsi_label.setWordWrap(True)  

        # Tombol Sunting
        sunting_btn = QPushButton("SUNTING")
        sunting_btn.setFixedSize(240, 60)
        sunting_btn.setFont(QFont("Inter", 12, QFont.Bold))
        sunting_btn.setStyleSheet(""" 
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
        sunting_btn.clicked.connect(lambda: self.tampilkanFormInput(True, jadwal))

        # Tombol Hapus
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(240, 60)
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
        hapus_btn.clicked.connect(lambda: self.hapusJadwal(jadwal))

        item_layout.addWidget(deskripsi_label)
        item_layout.addStretch()
        item_layout.addWidget(sunting_btn)
        item_layout.addWidget(hapus_btn)

        item_widget.setFixedHeight(100) 
        item_widget.setStyleSheet("""
                                    QWidget {
                                        background-color: white;
                                        border-radius: 16px;
                                        min-height: 60px;
                                        border: 1px solid #E0E0E0;
                                    }
                                    """)

        self.scroll_layout.addWidget(item_widget)

    def perbaruiTampilan(self):
        """Memperbarui tampilan setelah perubahan data"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for jadwal in self.__jadwal_list:
            self.jadwal_item(jadwal)

        self.scroll_layout.addStretch()

    def hapusJadwal(self, jadwal):
        confirm_dialog = DeleteConfirmDialog(self)
        if confirm_dialog.exec_() == QDialog.Accepted:
            if self.__kontrol_jadwal.hapusJadwal(jadwal['id']):
                self.kelolaJadwal()

    def tampilkanFormInput(self, is_edit=False, jadwal=None):
        form = FormInputJadwal(self, is_edit=is_edit, data=jadwal, kontrol_tanaman=self.__kontrol_tanaman)
        if form.exec_() == QDialog.Accepted:
            deskripsi = form.deskripsi_input.text()
            waktu = form.datetime_edit.dateTime().toPyDateTime()
            tanaman_id = form.tanaman_combo.currentData()  

            if is_edit and jadwal:
                self.__kontrol_jadwal.updateJadwal(jadwal['id'], deskripsi, waktu, tanaman_id)
            else:
                self.__kontrol_jadwal.tambahJadwal(deskripsi, waktu, tanaman_id)
            self.kelolaJadwal()