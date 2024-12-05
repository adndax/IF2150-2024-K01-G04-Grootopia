from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QDialog, QLineEdit, QCalendarWidget, QHBoxLayout,
                           QSpinBox, QFrame, QDateTimeEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QIcon
import os

class TanamanDialog(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Tanaman" if not is_edit else "Sunting Tanaman")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #DDE3D8;
                border-radius: 20px;
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
        layout.addWidget(title)
        
        # Nama Tanaman
        nama_label = QLabel("Nama Tanaman")
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        layout.addWidget(nama_label)
        
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Masukkan nama tanaman")
        self.nama_input.setFont(QFont("Inter", 12))
        self.nama_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 8px;
                min-height: 45px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.nama_input)
        
        # Waktu Tanam
        waktu_label = QLabel("Waktu Tanam")
        waktu_label.setFont(QFont("Inter", 12, QFont.Bold))
        layout.addWidget(waktu_label)
        
        waktu_container = QHBoxLayout()
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
        title.setFont(QFont("Inter", 14, QFont.Bold))
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

class KelolaTanaman(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Tambah Tanaman button
        tambah_btn = QPushButton("+ Tambah Tanaman")
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
        tambah_btn.clicked.connect(self.tampilkanFormInputTambah)
        layout.addWidget(tambah_btn)
        
        # Tanaman items
        self.tanaman_list = [
            {'id': 1, 'nama': 'Tanaman A', 'waktu_tanam': QDateTime.currentDateTime()},
            {'id': 2, 'nama': 'Tanaman B', 'waktu_tanam': QDateTime.currentDateTime()}
        ]
        
        for tanaman in self.tanaman_list:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(25, 15, 25, 15)
            item_layout.setSpacing(20)
            
            nama_label = QLabel(tanaman['nama'])
            nama_label.setFont(QFont("Inter", 12, QFont.Bold))
            nama_label.setStyleSheet("color: #6C4530; border: none;")
            
            sunting_btn = QPushButton("SUNTING")
            sunting_btn.setFixedSize(240, 40)
            sunting_btn.setFont(QFont("Inter", 12, QFont.Bold))
            sunting_btn.setStyleSheet("""
                QPushButton {
                    background-color: #59694D;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-weight: bold;
                    margin-bottom: 20px; 
                }
                QPushButton:hover {
                    background-color: #4a5a3e;
                }
            """)
            sunting_btn.clicked.connect(lambda checked, t=tanaman: self.tampilkanFormInputEdit(t))
            
            hapus_btn = QPushButton("HAPUS")
            hapus_btn.setFixedSize(240, 40)
            hapus_btn.setFont(QFont("Inter", 12, QFont.Bold))
            hapus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9B2C2C;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-weight: bold;
                    margin-bottom: 20px; 
                }
                QPushButton:hover {
                    background-color: #8b1c1c;
                }
            """)
            hapus_btn.clicked.connect(lambda checked, t=tanaman: self.tampilkanKonfirmasiDelete(t))
            
            item_layout.addWidget(nama_label)
            item_layout.addStretch()
            item_layout.addWidget(sunting_btn)
            item_layout.addWidget(hapus_btn)
            
            item_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border-radius: 16px;
                    min-height: 70px;
                    border: 1px solid #E0E0E0;
                }
            """)
            
            layout.addWidget(item_widget)
        
        layout.addStretch()
    
    def tampilkanFormInputTambah(self):
        dialog = TanamanDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Tambah tanaman")
    
    def tampilkanFormInputEdit(self, tanaman):
        dialog = TanamanDialog(self, is_edit=True, data=tanaman)
        if dialog.exec_() == QDialog.Accepted:
            print("Update tanaman:", tanaman['id'])
    
    def tampilkanKonfirmasiDelete(self, tanaman):
        dialog = DeleteConfirmDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Delete tanaman:", tanaman['id'])


