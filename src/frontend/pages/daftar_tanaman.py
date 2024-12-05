from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
class DaftarTanaman(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Daftar Tanaman"))
        self.setLayout(layout)