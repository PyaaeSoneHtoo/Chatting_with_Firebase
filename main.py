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
        # Main layout with background
        self.setStyleSheet("background-color: #f1f2f6;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login Card Container
        card = QWidget()
        card.setMinimumWidth(350)
        card.setMaximumWidth(400)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        # We need a slight shadow effect normally, but pure CSS shadow in Qt is limited
        # We will use clean borders instead
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(15)

        # Icon/Title
        title_label = QLabel("Welcome Back")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2f3640; margin-bottom: 10px;")
        
        subtitle_label = QLabel("Sign in to continue to Chat")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8fa6; margin-bottom: 20px;")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setFont(QFont("Segoe UI", 11))
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #f5f6fa;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                color: #2f3640;
            }
            QLineEdit:focus {
                border: 1px solid #4a69bd;
                background-color: white;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #f5f6fa;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                color: #2f3640;
            }
            QLineEdit:focus {
                border: 1px solid #4a69bd;
                background-color: white;
            }
        """)

        self.login_btn = QPushButton("Login")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a69bd; 
                color: white; 
                padding: 12px; 
                border-radius: 8px;
                border: none;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #3c5399;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)

        self.register_btn = QPushButton("Create an Account")
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.setFont(QFont("Segoe UI", 10))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: #4a69bd; 
                padding: 5px; 
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0c2461;
            }
        """)
        self.register_btn.clicked.connect(self.handle_register)

        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.register_btn)

        layout.addWidget(card)
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header area
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #4a69bd;
                border-bottom: 2px solid #3c5399;
            }
        """)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        self.user_label = QLabel("Logged in as: ...")
        self.user_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.user_label.setStyleSheet("color: white;")
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e55039; 
                color: white; 
                padding: 6px 15px; 
                border-radius: 15px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #eb2f06;
            }
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        
        # Chat Display area
        chat_container = QWidget()
        chat_container.setStyleSheet("background-color: #f1f2f6;")
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(15, 15, 15, 15)
        
        self.chat_display = QListWidget()
        self.chat_display.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: white;
                color: #2f3640;
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 8px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
        """)
        chat_layout.addWidget(self.chat_display)
        
        # Input Area
        input_widget = QWidget()
        input_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #dcdde1;
            }
        """)
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(10)
        
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type a message...")
        self.msg_input.setFont(QFont("Segoe UI", 13))
        self.msg_input.returnPressed.connect(self.send_message)
        self.msg_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px; 
                background-color: #f1f2f6;
                border: 1px solid #dcdde1; 
                border-radius: 20px;
                color: #2f3640;
            }
            QLineEdit:focus {
                border: 1px solid #4a69bd;
                background-color: #ffffff;
            }
        """)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a69bd; 
                color: white; 
                padding: 12px 25px; 
                border-radius: 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3c5399;
            }
            QPushButton:pressed {
                background-color: #0c2461;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(self.send_btn)
        
        layout.addWidget(header_widget)
        layout.addWidget(chat_container, stretch=1)
        layout.addWidget(input_widget)
        
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
