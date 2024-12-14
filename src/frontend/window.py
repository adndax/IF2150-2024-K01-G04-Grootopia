# src/frontend/window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer
from src.frontend.components.notification import Pemberitahuan  # Import Pemberitahuan
from src.backend.controllers.kontrol_jadwal import KontrolJadwal  # Backend untuk jadwal
from .pages.daftar_tanaman import TanamanUI
from .pages.catatan_perkembangan import CatatanPerkembangan
from .pages.jadwal_perawatan import JadwalUI
from src.frontend.components.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grootopia")
        self.setGeometry(100, 100, 1920, 1080)

        # Inisialisasi kontrol jadwal untuk pemberitahuan
        self.kontrol_jadwal = KontrolJadwal()

        # Layout utama
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        self.sidebar = Sidebar()
        self.sidebar.pageChanged.connect(self.change_page)

        self.stack = QStackedWidget()
        self.stack.addWidget(TanamanUI())  
        self.stack.addWidget(CatatanPerkembangan())
        self.stack.addWidget(JadwalUI())

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        # Inisialisasi notifikasi dan timer
        self.init_notifikasi()

    def init_notifikasi(self):
        """Mengatur pemberitahuan dan timer global"""
        self.notif = Pemberitahuan(id=1, nama="Notifikasi", waktu_perawatan=3600, last_perawatan=None)
        self.notif.kontrol_jadwal = self.kontrol_jadwal  # Sambungkan dengan kontrol jadwal
        
        # Timer untuk mengecek notifikasi setiap menit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.notif.cekNotifikasi)
        self.timer.start(60000)  # Interval 60 detik

    def change_page(self, index):
        self.stack.setCurrentIndex(index)