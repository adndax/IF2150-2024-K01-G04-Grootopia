from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
class CatatanPerkembangan(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Catatan Perkembangan"))
        self.setLayout(layout)