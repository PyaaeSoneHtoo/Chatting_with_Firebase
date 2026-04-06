# Firebase Chat App

A modern, sleek, and colorful desktop chat application built with **Python**, **PyQt6**, and **Firebase**. 

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![Firebase](https://img.shields.io/badge/Firebase-Backend-orange.svg)

## ✨ Features
* 🔐 **Authentication:** Secure user registration and login using Firebase Authentication.
* 💬 **Real-time Messaging:** Live chat room using Firebase Realtime Database.
* 🎨 **Modern UI:** Clean, card-based interface with customized inputs, buttons, and rounded chat bubbles.
* 🔄 **Auto-scrolling:** Automatically scrolls to the newest message in the chat display.

## 🛠️ Prerequisites
* Python 3.8 or higher.
* A Firebase Project with **Authentication** (Email/Password) and **Realtime Database** enabled.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PyaaeSoneHtoo/Chatting_with_Firebase.git
   cd Chatting_with_Firebase
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   Make sure you have installed the required packages (usually found in the workspace root `requirements.txt`):
   ```bash
   pip install PyQt6 pyrebase4 requests
   ```

4. **Configure Firebase:**
   Open `main.py` and locate the `firebaseConfig` dictionary at the top of the file. Replace it with your actual Firebase project credentials:
   ```python
   firebaseConfig = {
       "apiKey": "YOUR_API_KEY",
       "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
       "databaseURL": "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
       "projectId": "YOUR_PROJECT_ID",
       "storageBucket": "YOUR_PROJECT_ID.appspot.com",
       "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
       "appId": "YOUR_APP_ID",
       "measurementId": "YOUR_MEASUREMENT_ID"
   }
   ```
   *Note: Ensure your Realtime Database rules allow read/write access for authenticated users.*

## 💻 Usage
Run the application using Python:
```bash
python main.py
```

## 📄 License
This project is open-source and free to use.