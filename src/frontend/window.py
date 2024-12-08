# src/frontend/window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from .components.sidebar import Sidebar  
from .pages.daftar_tanaman import TanamanUI  # Ganti KelolaTanaman menjadi TanamanUI sesuai perubahan nama class sebelumnya
from .pages.catatan_perkembangan import CatatanPerkembangan
from .pages.jadwal_perawatan import JadwalPerawatan

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grootopia")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        self.sidebar = Sidebar()
        self.sidebar.pageChanged.connect(self.change_page)

        self.stack = QStackedWidget()
        self.stack.addWidget(TanamanUI())  
        self.stack.addWidget(CatatanPerkembangan())
        self.stack.addWidget(JadwalPerawatan())

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)