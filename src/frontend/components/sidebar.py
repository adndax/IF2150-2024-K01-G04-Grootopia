from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os

class Sidebar(QWidget):
    pageChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        current_file = os.path.abspath(__file__)
        frontend_dir = os.path.dirname(os.path.dirname(current_file))
        src_dir = os.path.dirname(frontend_dir)
        root_dir = os.path.dirname(src_dir)
        self.img_path = os.path.join(root_dir, 'img')
        self.setup_ui()
    def setup_ui(self):
        self.inter_font = QFont("Arial", 12, QFont.Bold)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Dashboard label
        dashboard_container = QWidget()
        dashboard_container.setStyleSheet("""
            background-color: #59694D; 
            border-radius: 0px;
            margin: 0px;
            padding: 10px 20px;
        """)
        dashboard_layout = QHBoxLayout(dashboard_container)
        dashboard_layout.setContentsMargins(15, 10, 15, 10)
        
        dashboard_label = QLabel("Dashboard")
        dashboard_label.setFont(self.inter_font)
        dashboard_label.setStyleSheet("color: white;")
        dashboard_layout.addWidget(dashboard_label)
        layout.addWidget(dashboard_container)
        
        # Container untuk konten utama dengan padding
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 40, 20)  # Tambah padding kanan
        content_layout.setSpacing(15)
        
        # Logo and Title
        logo_layout = QHBoxLayout()
        logo = QLabel()
        logo_path = os.path.join(self.img_path, 'logo.png')
        if os.path.exists(logo_path):
            logo_pixmap = QIcon(logo_path).pixmap(30, 30)
            logo.setPixmap(logo_pixmap)
        
        title = QLabel()
        title_font = QFont("Arial", 14, QFont.Bold)
        title.setFont(title_font)
        title.setText('<span style="color: #59694D;">Groo</span><span style="color: #6C4530;">topia</span>')
        title.setTextFormat(Qt.RichText)
        
        logo_layout.addWidget(logo)
        logo_layout.addWidget(title)
        logo_layout.addStretch()
        content_layout.addLayout(logo_layout)
        

        # Grow Happily! label with icon
        grow_layout = QHBoxLayout()
        grow_layout.setContentsMargins(8, 0, 0, 0)  # Sejajarkan dengan konten lain
        pucuk_icon = QLabel()
        pucuk_path = os.path.join(self.img_path, 'pucuk.svg')
        if os.path.exists(pucuk_path):
            pucuk_pixmap = QIcon(pucuk_path).pixmap(20, 20)
            pucuk_icon.setPixmap(pucuk_pixmap)

        grow_label = QLabel()
        grow_label.setFont(self.inter_font)
        grow_label.setText('<span style="color: #59694D;">Grow</span> <span style="color: #333333;">Happily!</span>')
        grow_label.setTextFormat(Qt.RichText)

        grow_layout.addWidget(pucuk_icon)
        grow_layout.addWidget(grow_label)
        grow_layout.addStretch()
        content_layout.addLayout(grow_layout)
        # Navigation buttons
        nav_items = [
            ("Tanaman", os.path.join(self.img_path, 'tanaman.svg')),
            ("Catatan Perkembangan", os.path.join(self.img_path, 'book.svg')),
            ("Jadwal Perawatan", os.path.join(self.img_path, 'calender.svg'))
        ]
        
        self.nav_buttons = []
        for idx, (text, icon_path) in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setFont(self.inter_font)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                btn.setIcon(icon)
                btn.setIconSize(QIcon(icon_path).pixmap(24, 24).size())
            
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 15px;
                    padding-right: 30px;
                    border: none;
                    border-radius: 12px;
                    color: #333333;
                    min-height: 50px;
                    min-width: 310px;
                    font-weight: bold;
                    margin-right: 20px;  /* Tambah margin kanan */
                }
                QPushButton:hover {
                    background-color: rgba(89, 105, 77, 0.1);
                }
                QPushButton:checked {
                    background-color: #59694D;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, i=idx: self.handle_button_click(i))
            
            content_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            
        content_layout.addStretch()
        layout.addWidget(content_container)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #EBF1E6;
            }
            QWidget#content {
                background-color: #EBF1E6;
            }
        """)
        content_container.setObjectName("content")     

        
    def handle_button_click(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.pageChanged.emit(index)

