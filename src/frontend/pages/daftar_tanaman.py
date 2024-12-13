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
                border-radius: 20px;
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
                border-radius: 8px;
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
                border-radius: 8px;
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
                border-radius: 12px;
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
        header_layout.setContentsMargins(30, 30, 30, 15)
        
        # Tambah Tanaman button
        tambah_btn = QPushButton("+ Tambah Tanaman")
        tambah_btn.setFixedHeight(50)
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
                background: #3D2929;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #3D2929;
                border-radius: 5px;
            }
        """)
        
        # Container untuk item-item tanaman
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setContentsMargins(30, 15, 30, 30)
        scroll.setWidget(self.scroll_content)
        
        self.__main_layout.addWidget(scroll)
        
        self.kelolaTanaman()

    def kelolaTanaman(self):
        self.__tanaman_list = self.__kontrol_tanaman.getDaftarTanaman()
        self.perbaruiTampilan()

    def tanaman_item(self, tanaman):
       
        item_widget = QWidget()
        item_widget.setFixedHeight(70)
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(25, 20, 25, 20)
        item_layout.setSpacing(20)
        
        nama_label = QLabel(tanaman['nama'])
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        nama_label.setAlignment(Qt.AlignHCenter)
        nama_label.setStyleSheet("""QLabel {
                                    color: #6C4530;
                                    border: none;
                                    margin-top: 10;
                                }
                            """)
        
        sunting_btn = QPushButton("SUNTING")
        sunting_btn.setFixedSize(100, 30)
        sunting_btn.setFont(QFont("Inter", 12, QFont.Bold))
        sunting_btn.setStyleSheet("""
            QPushButton {
                background-color: #59694D;
                color: white;
                border-radius: 12px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)
        sunting_btn.clicked.connect(lambda: self.tampilkanFormInput(True, tanaman))
        
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
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #8b1c1c;
            }
        """)
        hapus_btn.clicked.connect(lambda: self.tampilkanKonfirmasi(tanaman))
        
        item_layout.addWidget(nama_label)
        item_layout.addStretch()
        item_layout.addWidget(sunting_btn)
        item_layout.addWidget(hapus_btn)
        
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
                min-height: 70px;
            }
        """)
        
        self.scroll_layout.addWidget(item_widget)
        self.scroll_content.setStyleSheet("QWidget { min-height: 0px; }")

    def perbaruiTampilan(self):
        """Memperbarui tampilan setelah perubahan data"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for tanaman in self.__tanaman_list:
            self.tanaman_item(tanaman)
        
        self.scroll_layout.addStretch()
    
    def tampilkanFormInput(self, is_edit=False, data=None):
        dialog = FormInputTanaman(self, is_edit, data)
        if dialog.exec_() == QDialog.Accepted:
            nama = dialog.nama_input.text()
            waktu_tanam = dialog.datetime_edit.dateTime().toPyDateTime()
            success = False
            if is_edit:
                success = self.__kontrol_tanaman.prosesUpdateTanaman(data['id'], nama, waktu_tanam)
            else:
                success = self.__kontrol_tanaman.prosesTambahTanaman(nama, waktu_tanam)
            
            if success:
                self.__tanaman_list = self.__kontrol_tanaman.getDaftarTanaman()
                self.perbaruiTampilan()
    
    def tampilkanKonfirmasi(self, tanaman):
        dialog = DeleteConfirmDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            if self.__kontrol_tanaman.prosesHapusTanaman(tanaman['id']):
                self.__tanaman_list = self.__kontrol_tanaman.getDaftarTanaman()
                self.perbaruiTampilan()