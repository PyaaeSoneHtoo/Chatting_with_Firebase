import sys
import json
import pyrebase
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QStackedWidget, QListWidget,
                             QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont

# Firebase Configuration
# IMPORTANT: Replace this with your actual Firebase Project Configuration!
firebaseConfig = {
    "apiKey": "AIzaSyChP6LMzy-BNIVXKFP-UFx9DG9PTJGdnYc",
    "authDomain": "chatapp-8ca24.firebaseapp.com",
    "databaseURL": "https://chatapp-8ca24-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "chatapp-8ca24",
    "storageBucket": "chatapp-8ca24.firebasestorage.app",
    "messagingSenderId": "639036709963",
    "appId": "1:639036709963:web:db5df2a81adaaa875001ce",
    "measurementId": "G-91M600JQLZ"
}

# Initialize Firebase
try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
except Exception as e:
    print(f"Error initializing Firebase: {e}")

class LoginWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Welcome to Firebase Chat")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setMinimumWidth(250)
        self.email_input.setStyleSheet("padding: 5px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumWidth(250)
        self.password_input.setStyleSheet("padding: 5px;")

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold; border-radius: 4px;")
        self.login_btn.clicked.connect(self.handle_login)

        self.register_btn = QPushButton("Create Account")
        self.register_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px; font-weight: bold; border-radius: 4px;")
        self.register_btn.clicked.connect(self.handle_register)

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Email and Password are required!")
            return

        try:
            # Check if using placeholder config
            if firebaseConfig["apiKey"] == "YOUR_API_KEY":
                QMessageBox.warning(self, "Setup Required", "Please configure your Firebase credentials in main.py first.")
                return
                
            user = auth.sign_in_with_email_and_password(email, password)
            self.main_app.current_user = user
            self.main_app.show_chat_screen()
            self.email_input.clear()
            self.password_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Login Failed", str(e))

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Email and Password are required!")
            return
            
        try:
            if firebaseConfig["apiKey"] == "YOUR_API_KEY":
                QMessageBox.warning(self, "Setup Required", "Please configure your Firebase credentials in main.py first.")
                return
                
            user = auth.create_user_with_email_and_password(email, password)
            
            # Save simple user profile in database
            uid = user['localId']
            username = email.split('@')[0]
            db.child("users").child(uid).set({"username": username, "email": email})
            
            QMessageBox.information(self, "Success", "Account created successfully! You can now login.")
        except Exception as e:
            QMessageBox.warning(self, "Registration Failed", str(e))

class ChatWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.messages = []
        self.init_ui()
        
        # Setup polling for new messages
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_messages)
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        self.user_label = QLabel("Logged in as: ...")
        self.user_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px; border-radius: 3px;")
        self.logout_btn.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        
        # Chat Display
        self.chat_display = QListWidget()
        self.chat_display.setStyleSheet("""
            QListWidget {
                background-color: #f5f6fa;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #ecf0f1;
            }
        """)
        
        # Input Area
        input_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type a message...")
        self.msg_input.returnPressed.connect(self.send_message)
        self.msg_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px 15px; font-weight: bold; border-radius: 4px;")
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)

    def start_chat(self):
        if hasattr(self.main_app, 'current_user') and self.main_app.current_user:
            email = self.main_app.current_user.get('email', 'Unknown User')
            self.user_label.setText(f"Logged in as: {email}")
            self.chat_display.clear()
            self.messages = []
            
            # Start polling database every 2 seconds
            self.timer.start(2000)
            self.poll_messages()

    def handle_logout(self):
        self.timer.stop()
        self.main_app.current_user = None
        self.chat_display.clear()
        self.main_app.show_login_screen()

    def send_message(self):
        text = self.msg_input.text().strip()
        if not text:
            return
            
        try:
            if not self.main_app.current_user:
                return
                
            email = self.main_app.current_user.get('email', 'Unknown')
            username = email.split('@')[0]
            
            data = {
                "sender": username,
                "text": text,
                "timestamp": pyrebase.pyrebase.requests.get("https://us-central1-firebase-adminsdk-xxxxx.cloudfunctions.net/serverTime", verify=False).text if False else "Just now" # Simplification for timestamp
            }
            
            db.child("messages").push(data)
            self.msg_input.clear()
            self.poll_messages() # Immediate refresh
        except Exception as e:
            print(f"Error sending message: {e}")

    def poll_messages(self):
        try:
            # In a production app, you would use Pyrebase Streams.
            # For simplicity and stability with PyQt, we poll the last 50 messages
            all_messages = db.child("messages").order_by_key().limit_to_last(50).get()
            
            if not all_messages.each():
                return
                
            new_messages = []
            for msg in all_messages.each():
                new_messages.append((msg.key(), msg.val()))
                
            # If the length is different, update UI
            if len(new_messages) != len(self.messages):
                self.messages = new_messages
                self.update_chat_ui()
                
        except Exception as e:
            print(f"Error polling messages: {e}")

    def update_chat_ui(self):
        self.chat_display.clear()
        for key, msg_data in self.messages:
            sender = msg_data.get('sender', 'Unknown')
            text = msg_data.get('text', '')
            
            # Format message
            display_text = f"{sender}: {text}"
            self.chat_display.addItem(display_text)
            
        self.chat_display.scrollToBottom()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firebase Chat App")
        self.setMinimumSize(600, 800)
        
        self.current_user = None
        
        # Setup Stacked Widget for Screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.login_screen = LoginWindow(self)
        self.chat_screen = ChatWindow(self)
        
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.chat_screen)
        
        self.show_login_screen()

    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def show_chat_screen(self):
        self.stacked_widget.setCurrentWidget(self.chat_screen)
        self.chat_screen.start_chat()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Simple Global Stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        QLineEdit {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 5px;
            font-size: 14px;
        }
        QPushButton {
            font-size: 14px;
        }
    """)
    
    window = MainApp()
    window.show()
    sys.exit(app.exec())
