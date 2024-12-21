# PROGRAM K01-G04-Grootopia-UC04

# IDENTITAS
# Kelompok     : K01 - G04 - Groootopia
# NIM/Nama - 1 : 13523005 - Muhammad Alfansya
# NIM/Nama - 2 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 3 : 13523057 - Faqih Muhammad Syuhada
# NIM/Nama - 4 : 13523065 - Dzaky Aurellia Fawwaz
# NIM/Nama - 5 : 13523071 - Adinda Putri
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : notification.py
# Topik        : Tugas Besar Rekayasa Perangkat Lunak 2024 (IF2150-24)
# Tanggal      : Sabtu, 21 Desember 2024
# Deskripsi    : Subprogram UC04 - Pemberitahuan Perawatan Tanaman (Notifikasi)
# PJ UC04      : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# PyQt5 , datetime , os : module
# Pemberitahuan , KontrolPemberitahuan , NotificationWindow : class

# ALGORITMA
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPixmap , QFont , QIcon
from PyQt5.QtWidgets import QMainWindow , QLabel , QPushButton , QVBoxLayout , QWidget , QHBoxLayout , QFrame , QGraphicsDropShadowEffect , QApplication
from datetime import datetime , timedelta
from src.backend.controllers.kontrol_tanaman import *
from src.backend.controllers.kontrol_jadwal import *
import os

class Pemberitahuan :
    # SPESIFIKASI LOKAL
    # Kelas Notifikasi Entity.

    # KAMUS LOKAL
    # __init__ : procedure

    # ALGORITMA LOKAL
    def __init__(self , id , nama , waktu_tanam , jenis_perawatan , waktu_perawatan) :
        self.id = id
        self.nama = nama
        self.waktu_tanam = waktu_tanam
        self.jenis_perawatan = jenis_perawatan
        self.waktu_perawatan = timedelta(seconds = waktu_perawatan)

class KontrolPemberitahuan :
    # SPESIFIKASI LOKAL
    # Kelas Notifikasi Controller.

    # KAMUS LOKAL
    # processCekNotifikasi , cekNotifikasi : procedure

    # ALGORITMA LOKAL
    def processCekNotifikasi(self) :
        daftar_tanaman = KontrolTanaman.getDaftarTanaman()
        daftar_jadwal = KontrolJadwal.getDaftarJadwal()
        now = datetime.now()
        while (true) :
            for jadwal in daftar_jadwal :
                tanaman = Pemberitahuan(jadwal['tanaman_id'] , daftar_tanaman[jadwal['tanaman_id']]['__nama'] , daftar_tanaman[jadwal['tanaman_id']]['__waktu_tanam'] , jadwal['jenis_perawatan'] , jadwal['waktu'])
                if (tanaman.cekNotifikasi()) :
                    app = QApplication(sys.argv)
                    notif_window = NotificationWindow(tanaman.nama , tanaman.jenis_perawatan)
                    notif_window.show()
                    sys.exit(app.exec_())

    def cekNotifikasi(self) :
        now = datetime.now()
        target = (now - self.waktu_tanam) % self.waktu_perawatan
        return (target < timedelta(seconds = 1))

class NotificationWindow(QMainWindow) :
    # SPESIFIKASI LOKAL
    # Kelas Notifikasi UI / Boundary.

    # KAMUS LOKAL
    # __init__ , initUI , closeNotif , closeEvent : procedure

    # ALGORITMA LOKAL
    def __init__(self , nama_tanaman , jenis_perawatan) :
        super().__init__()
        self.nama_tanaman = nama_tanaman
        self.jenis_perawatan = jenis_perawatan
        self.initUI()

    def initUI(self) :
        logo_path = os.path.join(os.path.dirname(__file__) , 'logo.png')

        self.setWindowTitle("Grootopia")
        self.setFixedSize(1100 , 400)
        self.setStyleSheet("background-color : #E4E8DC")
        self.setWindowIcon(QIcon(logo_path))

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path).scaled(50 , 50 , Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)

        title_label = QLabel("<b>Groo<span style = 'color : #6C4530'>topia</span></b>")
        title_label.setFont(QFont("Inter" , 13))
        title_label.setStyleSheet("color : #59694D ; margin-left : 5px")

        close_button_x = QPushButton("\u00D7")
        close_button_x.setFont(QFont("Arial", 20))
        close_button_x.setStyleSheet("background-color : transparent ; color : #000000 ; border : none ; padding : 5px")
        close_button_x.clicked.connect(self.closeNotif)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_button_x)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #606D56 ; border-top : 75px solid #606D56")
        separator.setFixedHeight(2)

        message_label = QLabel(
            f"<p style = 'font-size : 32px ; color : #3D2929'><b>"
            f"Waktunya merawat <span style = 'color : #9B2C2C ; font-weight : bold'>{self.nama_tanaman}</span>!</b></p>"
            f"<p style = 'font-size : 24px ; color : #3D2929'><b>"
            f"Jenis Perawatan : <span style = 'color : #9B2C2C'>{self.jenis_perawatan}</span></b></p>"
        )
        message_label.setAlignment(Qt.AlignCenter)

        box_widget = QWidget()
        box_layout = QVBoxLayout()
        box_layout.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(message_label)

        close_button = QPushButton("TUTUP")
        close_button.setFont(QFont("Inter" , 9 , QFont.Bold))
        close_button.setStyleSheet("background-color : #59694D ; color : #FFFDE8 ; padding : 15px 75px ; border-radius : 12px")
        close_button.clicked.connect(self.closeNotif)

        box_layout.addWidget(close_button , alignment = Qt.AlignCenter)
        spacer = QWidget()
        spacer.setFixedHeight(10)
        box_layout.addWidget(spacer)
        box_widget.setLayout(box_layout)
        box_widget.setStyleSheet("background-color : #FDFFFC ; border-radius : 15px ; padding : 20px")

        shadow_effect_button = QGraphicsDropShadowEffect()
        shadow_effect_button.setOffset(2 , 2)
        shadow_effect_button.setBlurRadius(5)
        shadow_effect_button.setColor(Qt.gray)
        close_button.setGraphicsEffect(shadow_effect_button)

        shadow_effect_box = QGraphicsDropShadowEffect()
        shadow_effect_box.setOffset(2 , 2)
        shadow_effect_box.setBlurRadius(5)
        shadow_effect_box.setColor(Qt.gray)
        box_widget.setGraphicsEffect(shadow_effect_box)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(separator)
        main_layout.addStretch()
        main_layout.addWidget(box_widget)
        main_layout.addStretch()

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def closeNotif(self) :
        self.close()

    def closeEvent(self , event) :
        self.closeNotif()
        event.accept()