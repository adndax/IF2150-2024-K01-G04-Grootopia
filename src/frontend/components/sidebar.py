from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os

class Sidebar(QWidget):
    pageChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(350)  # Perlebar jadi 350px
        current_file = os.path.abspath(__file__)
        frontend_dir = os.path.dirname(os.path.dirname(current_file))
        src_dir = os.path.dirname(frontend_dir)
        root_dir = os.path.dirname(src_dir)
        self.img_path = os.path.join(root_dir, 'img')
        self.setup_ui()
        
    def setup_ui(self):
        self.inter_font = QFont("Arial", 12)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Dashboard label
        dashboard_container = QWidget()
        dashboard_container.setStyleSheet("""
            background-color: #59694D; 
            border-radius: 12px;
            margin-right: 0px;
            padding-right: 0px;
        """)
        dashboard_layout = QHBoxLayout(dashboard_container)
        dashboard_layout.setContentsMargins(15, 10, 15, 10)
        
        dashboard_label = QLabel("Dashboard")
        dashboard_label.setFont(self.inter_font)
        dashboard_label.setStyleSheet("color: white; font-weight: bold;")
        dashboard_layout.addWidget(dashboard_label)
        layout.addWidget(dashboard_container)
        
        # Logo and Title
        logo_layout = QHBoxLayout()
        logo = QLabel()
        logo_path = os.path.join(self.img_path, 'logo.png')
        if os.path.exists(logo_path):
            logo_pixmap = QIcon(logo_path).pixmap(30, 30)
            logo.setPixmap(logo_pixmap)
        
        title = QLabel()
        title_font = QFont("Arial", 14)
        title.setFont(title_font)
        title.setText('<span style="color: #59694D;">Groo</span><span style="color: #6C4530;">topia</span>')
        title.setTextFormat(Qt.RichText)
        
        logo_layout.addWidget(logo)
        logo_layout.addWidget(title)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)
        
        layout.addSpacing(25)
        
        # Navigation buttons
        nav_items = [
            ("Tanaman", os.path.join(self.img_path, 'tanaman.svg')),
            ("Catatan Perkembangan", os.path.join(self.img_path, 'book.svg')),
            ("Jadwal Perawatan", os.path.join(self.img_path, 'calender.svg'))
        ]
        
        self.nav_buttons = []
        for idx, (text, icon_path) in enumerate(nav_items):
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setContentsMargins(0, 0, 0, 0)
            # button_container.setStyleSheet("""
            #     QWidget {
            #         background: transparent; 
            #         border: none;
            #     }
            # """)
            button_layout.setSpacing(0)
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
                        border-top-right-radius: 12px;    
                        border-bottom-right-radius: 12px;
                        border-top-left-radius: 12px;
                        border-bottom-left-radius: 12px;
                        color: #333333;
                        min-height: 50px;
                        min-width: 310px;
                    }
                    QPushButton:hover {
                        background-color: #E8E8E8;
                    }
                    QPushButton:checked {
                        background-color: #59694D;
                        color: white;
                    }
                """)
                        
            # btn.setStyleSheet("""
            #     QPushButton {
            #         text-align: left;
            #         padding: 15px;
            #         padding-right: 30px;
            #         border: none;
            #         border-radius: 12px;
            #         color: #333333;
            #         min-height: 50px;
            #         min-width: 310px;
            #     }
            #     QPushButton:hover {
            #         background-color: #E8E8E8;
            #     }
            #     QPushButton:checked {
            #         background-color: #59694D;
            #         color: white;
            #     }
            # """)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, i=idx: self.handle_button_click(i))
            
            button_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            layout.addWidget(button_container)
            
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            
        layout.addStretch()
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            QWidget#sidebar {
                min-height: 100vh;
            }
        """)
        self.setObjectName("sidebar")
        
    def handle_button_click(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.pageChanged.emit(index)
