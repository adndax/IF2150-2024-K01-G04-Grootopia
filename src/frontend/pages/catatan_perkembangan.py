from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit,
    QLineEdit, QDialog, QHBoxLayout, QScrollArea, QMessageBox,QDateTimeEdit, QSpinBox
)
from src.backend.controllers.manajer_catatan import KontrolCatatanPerkembangan
from src.backend.controllers.kontrol_tanaman import KontrolTanaman
from datetime import datetime
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QIcon
import os

class CatatanPerkembangan(QWidget):
    def __init__(self, parent=None):
        self.__kontrol_catatan = KontrolCatatanPerkembangan()
        super().__init__(parent)

        # Main layout untuk seluruh widget
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        # Container untuk tombol Tambah
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(30, 30, 30, 10)

        # Judul "Tanaman"
        title_label = QLabel("Catatan Perkembangan Tanaman")
        title_label.setFont(QFont("Inter", 30, QFont.Bold))
        title_label.setStyleSheet("color: #59694D;")
        title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(title_label)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari perkembangan catatan tanaman...")
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
        self.search_bar.textChanged.connect(self.filter_perkembangan_tanaman)
        header_layout.addWidget(self.search_bar)

        self.__main_layout.addWidget(self.header_widget)

        # Tombol tambah catatan
        tambah_btn = QPushButton("+ Tambah Catatan")
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
        tambah_btn.clicked.connect(self.tambah_catatan)
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
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(30, 15, 30, 30)
        scroll.setWidget(self.scroll_content)
        
        self.__main_layout.addWidget(scroll)
        
        self.kelolaPerkembanganTanaman()

    def kelolaPerkembanganTanaman(self):
        self.__perkembangan_tanaman_list = self.__kontrol_catatan.getDaftarCatatan()
        self.filtered_list = self.__perkembangan_tanaman_list 
        self.update_daftar_catatan()
    
    def filter_perkembangan_tanaman(self, query):
        """Filter data berdasarkan input pencarian."""
        query = query.lower().strip() 
        self.filtered_list = [
            catatan for catatan in self.__perkembangan_tanaman_list
            if query in catatan['judul_catatan'].lower() or query in str(catatan['id'])
        ]
        self.update_daftar_catatan(filtered=True)

    def tanaman_item(self, catatan):
    
        item_widget = QWidget()
        item_widget.setFixedHeight(70)
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(25, 20, 25, 20)
        item_layout.setSpacing(20)
        
        nama_label = QLabel(catatan['judul_catatan'])
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
                border-radius: 10px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #4a5a3e;
            }
        """)
        sunting_btn.clicked.connect(lambda _, id=catatan['id']: self.edit_catatan(id))
        
        hapus_btn = QPushButton("HAPUS")
        hapus_btn.setFixedSize(100, 30)
        hapus_btn.setFont(QFont("Inter", 12, QFont.Bold))
        hapus_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B2C2C;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #8b1c1c;
            }
        """)
        hapus_btn.clicked.connect(lambda _, id=catatan['id']: self.hapus_catatan(id))
        
        item_layout.addWidget(nama_label)
        item_layout.addStretch()
        item_layout.addWidget(sunting_btn)
        item_layout.addWidget(hapus_btn)
        
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
                min-height: 70px;
            }
        """)
        
        self.scroll_layout.addWidget(item_widget)
        self.scroll_content.setStyleSheet("QWidget { min-height: 0px; }")

    def tambah_catatan(self):
        dialog = FormInputCatatan(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # Proses hapus catatan
            data = dialog.get_data()
            sukses = self.__kontrol_catatan.prosesTambahCatatan(
                tanaman_id=1,  # Ganti dengan ID tanaman sesuai konteks
                judul_catatan=data["judul_catatan"],
                tanggal_perkembangan=datetime.now(),
                tinggi=100,  # Contoh nilai tinggi
                kondisi="Baik",  # Contoh nilai kondisi
                catatan=data["catatan"]
            )
            
            # Membuat dialog sukses/gagal
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Sukses" if sukses else "Gagal")
            result_dialog.setFixedSize(400, 250)
            result_dialog.setStyleSheet("background-color: #DDE3D8;")
            
            result_layout = QVBoxLayout(result_dialog)
            result_layout.setSpacing(30)
            result_layout.setContentsMargins(30, 35, 30, 35)
            
            # Title
            result_title = QLabel("SUKSES" if sukses else "GAGAL")
            result_title.setAlignment(Qt.AlignCenter)
            result_title.setFont(QFont("Inter", 16, QFont.Bold))
            result_title.setStyleSheet("color: #3D2929")
            result_layout.addWidget(result_title)
            
            # Info text
            result_text = QLabel(
                "Catatan berhasil ditambahkan!" if sukses else "Gagal menambah catatan!"
            )
            result_text.setAlignment(Qt.AlignCenter)
            result_text.setFont(QFont("Inter", 14, QFont.Bold))
            result_text.setStyleSheet("color: #3D2929")
            result_layout.addWidget(result_text)
            
            # Tombol OK
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
            ok_btn.clicked.connect(result_dialog.accept)
            
            button_layout = QHBoxLayout()
            button_layout.addWidget(ok_btn)
            button_layout.setAlignment(Qt.AlignCenter)
            result_layout.addLayout(button_layout)
            
            # Tampilkan dialog hasil
            result_dialog.exec_()
            
            # Refresh daftar catatan jika sukses
            if sukses:
                self.kelolaPerkembanganTanaman()

    def edit_catatan(self, id_catatan):
        daftar_catatan = self.__kontrol_catatan.getDaftarCatatan()
        data = next((c for c in daftar_catatan if c["id"] == id_catatan), None)
        if data:
            dialog = FormInputCatatan(parent=self, is_edit=True, data=data)
            if dialog.exec_() == QDialog.Accepted:
                # Proses hapus catatan
                updated_data = dialog.get_data()
                sukses = self.__kontrol_catatan.prosesUpdateCatatan(
                    id=id_catatan,
                    tanaman_id=data["tanaman_id"],
                    judul_catatan=updated_data["judul_catatan"],
                    tanggal_perkembangan=["tanggal_perkembangan"],
                    tinggi=updated_data["tinggi"],
                    kondisi=updated_data["kondisi"],
                    catatan=updated_data["catatan"]
                )
                
                # Membuat dialog sukses/gagal
                result_dialog = QDialog(self)
                result_dialog.setWindowTitle("Sukses" if sukses else "Gagal")
                result_dialog.setFixedSize(400, 250)
                result_dialog.setStyleSheet("background-color: #DDE3D8;")
                
                result_layout = QVBoxLayout(result_dialog)
                result_layout.setSpacing(30)
                result_layout.setContentsMargins(30, 35, 30, 35)
                
                # Title
                result_title = QLabel("SUKSES" if sukses else "GAGAL")
                result_title.setAlignment(Qt.AlignCenter)
                result_title.setFont(QFont("Inter", 16, QFont.Bold))
                result_title.setStyleSheet("color: #3D2929")
                result_layout.addWidget(result_title)
                
                # Info text
                result_text = QLabel(
                    "Catatan berhasil disunting!" if sukses else "Gagal menyunting catatan!"
                )
                result_text.setAlignment(Qt.AlignCenter)
                result_text.setFont(QFont("Inter", 14, QFont.Bold))
                result_text.setStyleSheet("color: #3D2929")
                result_layout.addWidget(result_text)
                
                # Tombol OK
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
                ok_btn.clicked.connect(result_dialog.accept)
                
                button_layout = QHBoxLayout()
                button_layout.addWidget(ok_btn)
                button_layout.setAlignment(Qt.AlignCenter)
                result_layout.addLayout(button_layout)
                
                # Tampilkan dialog hasil
                result_dialog.exec_()
                
                # Refresh daftar catatan jika sukses
                if sukses:
                    self.kelolaPerkembanganTanaman()

    def hapus_catatan(self, id_catatan):
        # Membuat dialog konfirmasi
        dialog = QDialog(self)
        dialog.setWindowTitle("Konfirmasi")
        dialog.setFixedSize(400, 450)
        dialog.setStyleSheet("background-color: #DDE3D8;")
        
        layout = QVBoxLayout(dialog)
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
        batal_btn.clicked.connect(dialog.reject)
        
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
        hapus_btn.clicked.connect(dialog.accept)
        
        button_layout.addWidget(batal_btn)
        button_layout.addWidget(hapus_btn)
        button_layout.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(button_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            # Proses hapus catatan
            sukses = self.__kontrol_catatan.prosesHapusCatatan(id_catatan)
            
            # Membuat dialog sukses/gagal
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Sukses" if sukses else "Gagal")
            result_dialog.setFixedSize(400, 250)
            result_dialog.setStyleSheet("background-color: #DDE3D8;")
            
            result_layout = QVBoxLayout(result_dialog)
            result_layout.setSpacing(30)
            result_layout.setContentsMargins(30, 35, 30, 35)
            
            # Title
            result_title = QLabel("SUKSES" if sukses else "GAGAL")
            result_title.setAlignment(Qt.AlignCenter)
            result_title.setFont(QFont("Inter", 16, QFont.Bold))
            result_title.setStyleSheet("color: #3D2929")
            result_layout.addWidget(result_title)
            
            # Info text
            result_text = QLabel(
                "Catatan berhasil dihapus!" if sukses else "Gagal menghapus catatan!"
            )
            result_text.setAlignment(Qt.AlignCenter)
            result_text.setFont(QFont("Inter", 14, QFont.Bold))
            result_text.setStyleSheet("color: #3D2929")
            result_layout.addWidget(result_text)
            
            # Tombol OK
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
            ok_btn.clicked.connect(result_dialog.accept)
            
            button_layout = QHBoxLayout()
            button_layout.addWidget(ok_btn)
            button_layout.setAlignment(Qt.AlignCenter)
            result_layout.addLayout(button_layout)
            
            # Tampilkan dialog hasil
            result_dialog.exec_()
            
            # Refresh daftar catatan jika sukses
            if sukses:
                self.kelolaPerkembanganTanaman()

    def update_daftar_catatan(self, filtered=False):
        """Memperbarui tampilan setelah perubahan data"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for tanaman in self.filtered_list:
            self.tanaman_item(tanaman)
        
        self.scroll_layout.addStretch()


class FormInputCatatan(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None):
        super(FormInputCatatan, self).__init__(parent)
        self.setWindowTitle("Tambah Tanaman" if not is_edit else "Sunting Tanaman")
        self.setFixedSize(1000, 800)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #DDE3D8;
                border-radius: 10px;
                color: #6C4530;
            }
        """)

        self.kontrol_tanaman = KontrolTanaman() 
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

        # Input Fields

        # ID Tanaman (dropdown)
        nama_label = QLabel("Nama Tanaman")
        nama_label.setFont(QFont("Inter", 12, QFont.Bold))
        nama_label.setStyleSheet("color: #3D2929")
        layout.addWidget(nama_label)

        self.tanaman_id_input = QComboBox(self)
        self.tanaman_id_input.setFont(QFont("Inter", 12))
        self.tanaman_id_input.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.tanaman_id_input)

        # Ambil daftar tanaman dari database
        tanaman_list = self.kontrol_tanaman.getDaftarTanaman()
        for tanaman in tanaman_list:
            # Masukkan nama tanaman ke dropdown, simpan ID sebagai data
            self.tanaman_id_input.addItem(tanaman['nama'], tanaman['id'])

        # Judul Catatan
        judul_catatan_label = QLabel("Judul Catatan")
        judul_catatan_label.setFont(QFont("Inter", 12, QFont.Bold))
        judul_catatan_label.setStyleSheet("color: #3D2929")
        layout.addWidget(judul_catatan_label)

        self.judul_catatan_input = QLineEdit(self)
        self.judul_catatan_input.setPlaceholderText("Masukkan Judul Catatan")
        self.judul_catatan_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.judul_catatan_input)

        # Tanggal Perkembangan
        tanggal_perkembangan_label = QLabel("Tanggal Perkembangan")
        tanggal_perkembangan_label.setFont(QFont("Inter", 12, QFont.Bold))
        tanggal_perkembangan_label.setStyleSheet("color: #3D2929")
        layout.addWidget(tanggal_perkembangan_label)

        tanggal_perkembangan_container = QHBoxLayout()
        self.tanggal_perkembangan_input = QDateTimeEdit(self)
        self.tanggal_perkembangan_input.setDateTime(QDateTime.currentDateTime())
        self.tanggal_perkembangan_input.setFont(QFont("Inter", 12))
        self.tanggal_perkembangan_input.setStyleSheet("""
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
        self.tanggal_perkembangan_input.setCalendarPopup(True)
        self.tanggal_perkembangan_input.setDisplayFormat("dd/MM/yyyy HH:mm")

        tanggal_perkembangan_container.addWidget(self.tanggal_perkembangan_input)
        layout.addWidget(self.tanggal_perkembangan_input)

        # Tinggi Input
        tinggi_label = QLabel("Tinggi Tanaman")
        tinggi_label.setFont(QFont("Inter", 12, QFont.Bold))
        tinggi_label.setStyleSheet("color: #3D2929")
        layout.addWidget(tinggi_label)

        self.tinggi_input = QSpinBox(self)
        self.tinggi_input.setRange(0, 1000)  # Tinggi maksimum 1000 cm
        self.tinggi_input.setPrefix("Tinggi: ")
        self.tinggi_input.setFont(QFont("Inter", 12))
        self.tinggi_input.setStyleSheet("""
            QSpinBox {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.tinggi_input)

        # Kondisi Input
        kondisi_label = QLabel("Kondisi Tanaman")
        kondisi_label.setFont(QFont("Inter", 12, QFont.Bold))
        kondisi_label.setStyleSheet("color: #3D2929")
        layout.addWidget(kondisi_label)

        self.kondisi_input = QComboBox(self)
        self.kondisi_input.addItems(["Baik", "Sedang", "Buruk"])
        self.kondisi_input.setFont(QFont("Inter", 12))
        self.kondisi_input.setStyleSheet("""
            QComboBox{
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.kondisi_input)

        # Catatan Input
        catatan_label = QLabel("Catatan Tanaman")
        catatan_label.setFont(QFont("Inter", 12, QFont.Bold))
        catatan_label.setStyleSheet("color: #3D2929")
        layout.addWidget(catatan_label)

        self.catatan_input = QTextEdit(self)
        self.catatan_input.setPlaceholderText("Masukkan Catatan")
        self.catatan_input.setFont(QFont("Inter", 12))
        self.catatan_input.setStyleSheet("""
            QTextEdit {
                padding: 12px;
                background: white;
                border-radius: 10px;
                min-height: 30px;
                font-size: 14px;
                color: #3D2929;
            }
        """)
        layout.addWidget(self.catatan_input)
        
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
        
        if is_edit and data:
            self.tanaman_id_input.setCurrentText(str(data["tanaman_id"]))
            self.judul_catatan_input.setText(data["judul_catatan"])
            self.tanggal_perkembangan_input.setDateTime(data["tanggal_perkembangan"])
            self.tinggi_input.setValue(data["tinggi"])
            self.kondisi_input.setCurrentText(data["kondisi"])
            self.catatan_input.setText(data["catatan"])

    def tampilkanFormInputCatatan(self, is_edit=False, data=None):
        dialog = FormInputCatatan(self, is_edit, data)
        if dialog.exec_() == QDialog.Accepted:
            tanaman_id = int(dialog.tanaman_id_input.text())
            judul_catatan = dialog.judul_catatan_input.text()
            tanggal_perkembangan = dialog.tanggal_perkembangan_input.dateTime().toPyDateTime()
            tinggi = dialog.tinggi_input.value()
            kondisi = dialog.kondisi_input.currentText()
            catatan = dialog.catatan_input.toPlainText()
            
            success = False
            if is_edit:
                success = self.__kontrol_catatan.prosesUpdateCatatan(data["id"], tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan)
            else:
                success = self.__kontrol_catatan.prosesTambahCatatan(tanaman_id, judul_catatan, tanggal_perkembangan, tinggi, kondisi, catatan)
            
            if success:
                self.__catatan_list = self.__kontrol_catatan.getDaftarCatatan()
                self.perbaruiTampilan()
            else:
                result_dialog = QDialog(self)
                result_dialog.setWindowTitle("Kesalahan")
                result_dialog.setFixedSize(400, 250)
                result_dialog.setStyleSheet("background-color: #DDE3D8;")
                
                result_layout = QVBoxLayout(result_dialog)
                result_layout.setSpacing(30)
                result_layout.setContentsMargins(30, 35, 30, 35)
                
                # Title
                result_title = QLabel("KESALAHAN")
                result_title.setAlignment(Qt.AlignCenter)
                result_title.setFont(QFont("Inter", 16, QFont.Bold))
                result_title.setStyleSheet("color: #3D2929")
                result_layout.addWidget(result_title)
                
                # Info text
                result_text = QLabel(
                    "Gagal menyimpan catatan perkembangan!"
                )
                result_text.setAlignment(Qt.AlignCenter)
                result_text.setFont(QFont("Inter", 14, QFont.Bold))
                result_text.setStyleSheet("color: #3D2929")
                result_layout.addWidget(result_text)
                
                # Tombol OK
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
                ok_btn.clicked.connect(result_dialog.accept)
                
                button_layout = QHBoxLayout()
                button_layout.addWidget(ok_btn)
                button_layout.setAlignment(Qt.AlignCenter)
                result_layout.addLayout(button_layout)
                
                # Tampilkan dialog hasil
                result_dialog.exec_()

        
    def get_data(self):
        return {
            "tanaman_id": self.tanaman_id_input.currentData(),  # Ambil ID tanaman dari dropdown
            "judul_catatan": self.judul_catatan_input.text(),
            "tanggal_perkembangan": self.tanggal_perkembangan_input.dateTime().toPyDateTime(),
            "tinggi": self.tinggi_input.value(),
            "kondisi": self.kondisi_input.currentText(),
            "catatan": self.catatan_input.toPlainText()
        }