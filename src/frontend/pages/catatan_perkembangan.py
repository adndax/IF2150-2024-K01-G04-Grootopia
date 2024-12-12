from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit,
    QLineEdit, QDialog, QHBoxLayout, QScrollArea, QMessageBox,QDateTimeEdit, QSpinBox
)
from src.backend.controllers.manajer_catatan import KontrolCatatanPerkembangan
from datetime import datetime
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont


class CatatanPerkembangan(QWidget):
    def __init__(self, parent=None):
        self.__kontrol_catatan = KontrolCatatanPerkembangan()
        super().__init__(parent)

        # Main layout untuk seluruh widget
        # self.__main_layout = QVBoxLayout(self)
        # self.__main_layout.setSpacing(0)
        # self.__main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setWindowTitle("Catatan Perkembangan")
        self.setMinimumSize(800, 600)
        self.catatan = {}  # Simpan catatan dalam dictionary {id: {"judul": str, "deskripsi": str}}
        self.id_counter = 1

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("Kelola Catatan Perkembangan")
        header.setFont(QFont("Inter", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Tombol tambah catatan
        tambah_btn = QPushButton("Tambah Catatan")
        tambah_btn.setFont(QFont("Inter", 12, QFont.Bold))
        tambah_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        tambah_btn.clicked.connect(self.tambah_catatan)
        layout.addWidget(tambah_btn)

        # Area daftar catatan
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

    def tambah_catatan(self):
        dialog = FormInputCatatan(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # Panggil backend untuk menambahkan catatan
            sukses = self.__kontrol_catatan.prosesTambahCatatan(
                tanaman_id=1,  # Ganti dengan ID tanaman sesuai konteks
                judul_catatan=data["judul"],
                tanggal_perkembangan=datetime.now(),
                tinggi=100,  # Contoh nilai tinggi
                kondisi="Baik",  # Contoh nilai kondisi
                catatan=data["deskripsi"]
            )
            if sukses:
                QMessageBox.information(self, "Sukses", "Catatan berhasil ditambahkan!")
                self.update_daftar_catatan()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal menambahkan catatan.")

    def lihat_catatan(self, id_catatan):
        if id_catatan in self.catatan:
            data = self.catatan[id_catatan]
            QMessageBox.information(self, f"Catatan ID {id_catatan}", f"Judul: {data['judul']}\nDeskripsi:\n{data['deskripsi']}")
        else:
            QMessageBox.warning(self, "Error", "Catatan tidak ditemukan!")

    def edit_catatan(self, id_catatan):
        daftar_catatan = self.__kontrol_catatan.getDaftarCatatan()
        data = next((c for c in daftar_catatan if c["id"] == id_catatan), None)
        if data:
            dialog = FormCatatan(parent=self, data={"judul": data["judul_catatan"], "deskripsi": data["catatan"]})
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_data()
                sukses = self.__kontrol_catatan.prosesUpdateCatatan(
                    id=id_catatan,
                    tanaman_id=1,  # Ganti dengan ID tanaman sesuai konteks
                    judul_catatan=updated_data["judul"],
                    tanggal_perkembangan=datetime.now(),
                    tinggi=120,  # Contoh nilai tinggi
                    kondisi="Sedang",  # Contoh nilai kondisi
                    catatan=updated_data["deskripsi"]
                )
                if sukses:
                    QMessageBox.information(self, "Sukses", "Catatan berhasil diperbarui!")
                    self.update_daftar_catatan()
                else:
                    QMessageBox.warning(self, "Gagal", "Gagal memperbarui catatan.")

    def hapus_catatan(self, id_catatan):
        sukses = self.__kontrol_catatan.prosesHapusCatatan(id_catatan)
        if sukses:
            QMessageBox.information(self, "Sukses", "Catatan berhasil dihapus!")
            self.update_daftar_catatan()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menghapus catatan.")

    def update_daftar_catatan(self):
        daftar_catatan = self.__kontrol_catatan.getDaftarCatatan()
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for catatan in daftar_catatan:
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(10, 10, 10, 10)

            judul_label = QLabel(f"ID {catatan['id']}: {catatan['judul_catatan']}")
            judul_label.setFont(QFont("Inter", 12))
            item_layout.addWidget(judul_label)

            lihat_btn = QPushButton("Lihat")
            lihat_btn.clicked.connect(lambda _, id=catatan['id']: self.lihat_catatan(id))
            item_layout.addWidget(lihat_btn)

            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, id=catatan['id']: self.edit_catatan(id))
            item_layout.addWidget(edit_btn)

            hapus_btn = QPushButton("Hapus")
            hapus_btn.clicked.connect(lambda _, id=catatan['id']: self.hapus_catatan(id))
            item_layout.addWidget(hapus_btn)

            self.scroll_layout.addWidget(item)



class FormInputCatatan(QDialog):
    def __init__(self, parent=None, is_edit=False, data=None):
        super(FormInputCatatan, self).__init__(parent)
        self.setWindowTitle("Form Catatan Perkembangan" + (" (Edit)" if is_edit else " (Tambah)"))
        self.setGeometry(100, 100, 400, 300)
        
        self.is_edit = is_edit
        self.data = data
        
        # Layout
        layout = QVBoxLayout(self)
        
        # Input Fields
        self.tanaman_id_input = QLineEdit(self)
        self.tanaman_id_input.setPlaceholderText("ID Tanaman")
        layout.addWidget(self.tanaman_id_input)

        self.judul_catatan_input = QLineEdit(self)
        self.judul_catatan_input.setPlaceholderText("Judul Catatan")
        layout.addWidget(self.judul_catatan_input)

        self.tanggal_perkembangan_input = QDateTimeEdit(self)
        self.tanggal_perkembangan_input.setDateTime(QDateTime.currentDateTime())
        self.tanggal_perkembangan_input.setCalendarPopup(True)
        layout.addWidget(self.tanggal_perkembangan_input)

        self.tinggi_input = QSpinBox(self)
        self.tinggi_input.setRange(0, 1000)  # Tinggi maksimum 1000 cm
        self.tinggi_input.setPrefix("Tinggi: ")
        layout.addWidget(self.tinggi_input)

        self.kondisi_input = QComboBox(self)
        self.kondisi_input.addItems(["Baik", "Sedang", "Buruk"])
        layout.addWidget(self.kondisi_input)

        self.catatan_input = QTextEdit(self)
        self.catatan_input.setPlaceholderText("Catatan")
        layout.addWidget(self.catatan_input)
        
        # Buttons
        self.submit_button = QPushButton("Simpan", self)
        self.submit_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.submit_button)
        
        self.cancel_button = QPushButton("Batal", self)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        
        # Pre-fill data if editing
        if is_edit and data:
            self.tanaman_id_input.setText(str(data["tanaman_id"]))
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
                QMessageBox.warning(self, "Kesalahan", "Gagal menyimpan catatan perkembangan.")
    def validate_and_accept(self):
        # Validasi input
        if not self.tanaman_id_input.text().isdigit():
            QMessageBox.warning(self, "Validasi Gagal", "ID Tanaman harus berupa angka.")
            return
        
        if not self.judul_catatan_input.text():
            QMessageBox.warning(self, "Validasi Gagal", "Judul Catatan tidak boleh kosong.")
            return

        if not self.catatan_input.toPlainText():
            QMessageBox.warning(self, "Validasi Gagal", "Catatan tidak boleh kosong.")
            return

        # Jika validasi berhasil
        self.accept()

        

    def get_data(self):
        return {
            "judul": self.judul_catatan_input.text(),  # Use the correct field name
            "deskripsi": self.catatan_input.toPlainText(),  # Use the correct field name
            "tinggi": self.tinggi_input.value(),  # Ensure it is numeric, so use .value()
            "kondisi": self.kondisi_input.currentText()  # Use currentText() to get the selected value
        }