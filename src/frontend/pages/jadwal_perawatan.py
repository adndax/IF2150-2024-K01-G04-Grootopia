from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class JadwalPerawatan(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Jadwal Perawatan"))
        self.setLayout(layout)
