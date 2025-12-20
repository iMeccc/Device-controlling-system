import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer

# Configuration
API_URL = "http://localhost:8000/api/v1"
INSTRUMENT_ID = 1  # This should be configured per machine

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_lock_mode()

    def initUI(self):
        self.setWindowTitle('Instrument Access Control')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('Please Login to Access Instrument')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)

    def setup_lock_mode(self):
        """
        Set window to be always on top and remove window decorations
        to simulate a lock screen.
        """
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        # In a real deployment, you would also want to hook keyboard events to block Alt+Tab, etc.
        # self.showFullScreen() 

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # TODO: Call backend API to verify credentials and reservation
        # response = requests.post(f"{API_URL}/login", json={...})
        
        # Mock success for now
        if username == "admin" and password == "admin":
            self.unlock_system()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials or no reservation found.')

    def unlock_system(self):
        """
        Hide the lock screen and start the monitoring timer.
        """
        self.hide()
        print("System Unlocked")
        # Start background monitoring service here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
