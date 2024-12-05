# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
#                            QHBoxLayout, QFrame)
# from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5.QtGui import QFont, QIcon
# import os

# class Sidebar(QWidget):
#     pageChanged = pyqtSignal(int)
    
#     def __init__(self):
#         super().__init__()
#         self.setFixedWidth(200)
#         current_file = os.path.abspath(__file__)  
#         frontend_dir = os.path.dirname(os.path.dirname(current_file))  
#         src_dir = os.path.dirname(frontend_dir)  
#         root_dir = os.path.dirname(src_dir)  
#         self.img_path = os.path.join(root_dir, 'img') 
        
#         print(f"Image path: {self.img_path}")  # Debug print
#         self.setup_ui()
        
#     def setup_ui(self):
#         # for img in ['logo.png', 'tanaman.svg', 'book.svg', 'calender.svg']:
#         #     full_path = os.path.join(self.img_path, img)
#         #     print(f"Checking {full_path}: {os.path.exists(full_path)}")

#         self.inter_font = QFont("Arial", 10)
        
#         layout = QVBoxLayout(self)
#         layout.setSpacing(10)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         # Dashboard label
#         dashboard_label = QLabel("Dashboard")
#         dashboard_label.setFont(self.inter_font)
#         dashboard_label.setStyleSheet("color: #59694D; font-weight: bold;")
#         layout.addWidget(dashboard_label)
        
#         # Logo and Title
#         logo_layout = QHBoxLayout()
#         logo = QLabel()
#         logo_path = os.path.join(self.img_path, 'logo.png')
#         if os.path.exists(logo_path):
#             logo_pixmap = QIcon(logo_path).pixmap(24, 24)
#             logo.setPixmap(logo_pixmap)
#         else:
#             print(f"Logo not found at: {logo_path}")
        
#         title = QLabel()
#         title.setFont(self.inter_font)
#         title.setText('<span style="color: #59694D;">Groo</span><span style="color: #6C4530;">topia</span>')
#         title.setTextFormat(Qt.RichText)
        
#         logo_layout.addWidget(logo)
#         logo_layout.addWidget(title)
#         logo_layout.addStretch()
#         layout.addLayout(logo_layout)
        
#         layout.addSpacing(20)
        
#         # Navigation buttons with error handling for icons
#         nav_items = [
#             ("Tanaman", os.path.join(self.img_path, 'tanaman.svg')),
#             ("Catatan Perkembangan", os.path.join(self.img_path, 'book.svg')),
#             ("Jadwal Perawatan", os.path.join(self.img_path, 'calender.svg'))
#         ]
        
#         self.nav_buttons = []
#         for idx, (text, icon_path) in enumerate(nav_items):
#             btn = QPushButton(text)
#             btn.setFont(self.inter_font)
#             if os.path.exists(icon_path):
#                 btn.setIcon(QIcon(icon_path))
#             else:
#                 print(f"Icon not found at: {icon_path}")
            
#             btn.setStyleSheet("""
#                 QPushButton {
#                     text-align: left;
#                     padding: 10px;
#                     border: none;
#                     border-radius: 12px;
#                     color: #333333;
#                 }
#                 QPushButton:hover {
#                     background-color: #E8E8E8;
#                 }
#                 QPushButton:checked {
#                     background-color: #59694D;
#                     color: white;
#                 }
#             """)
#             btn.setCheckable(True)
#             btn.setFixedHeight(40)
#             btn.clicked.connect(lambda checked, i=idx: self.handle_button_click(i))
#             self.nav_buttons.append(btn)
#             layout.addWidget(btn)
            
#         if self.nav_buttons:
#             self.nav_buttons[0].setChecked(True)
            
#         layout.addStretch()
        
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: white;
#                 border-top-right-radius: 20px;
#                 border-bottom-right-radius: 20px;
#             }
#         """)
        
#     def handle_button_click(self, index):
#         for i, btn in enumerate(self.nav_buttons):
#             btn.setChecked(i == index)
#         self.pageChanged.emit(index)