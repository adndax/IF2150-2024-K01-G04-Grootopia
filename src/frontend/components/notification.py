import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class Notification(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grootopia")
        self.setWindowIcon(QIcon("../../../img/logo.png"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        main_layout = QVBoxLayout()

        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: #f2f2f2; padding: 10px; border-bottom: 1px solid #ddd")
        title_layout = QVBoxLayout()

        title_label = QLabel("Grootopia")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        close_button = QPushButton("X")
        close_button.setStyleSheet("background-color: transparent; border: none; font-size: 12px; color: #333;")
        close_button.clicked.connect(self.close)

        title_layout.addWidget(title_label)
        title_layout.addWidget(close_button, alignment=Qt.AlignRight)
        title_frame.setLayout(title_layout)

        message_frame = QFrame()
        message_frame.setStyleSheet("background-color: white; padding: 15px; border-radius: 5px;")
        message_layout = QVBoxLayout()

        message_label = QLabel("Waktunya merawat {Nama Tanaman}!")
        message_label.setFont(QFont("Arial", 10))

        button = QPushButton("TUTUP")
        button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 12px;")
        button.clicked.connect(self.close)

        message_layout.addWidget(message_label)
        message_layout.addWidget(button, alignment=Qt.AlignCenter)
        message_frame.setLayout(message_layout)

        main_layout.addWidget(title_frame)
        main_layout.addWidget(message_frame)
        self.setLayout(main_layout)

        self.setGeometry(100, 100, 300, 200)