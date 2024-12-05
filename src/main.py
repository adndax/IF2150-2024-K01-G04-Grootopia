# src/main.py
# src/main.py
import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication
from frontend.window import MainWindow


def main():
    app = QApplication(sys.argv)
    # Inisialisasi backend services
    
    # Start frontend
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()