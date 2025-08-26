# Terminal TCP Chat

A Python-based multi-user chat application over TCP sockets, built as a **learning project** to explore:
- Network programming (sockets, TCP)
- User authentication and password hashing
- Public tunneling with **ngrok**
- Secure multi-threaded client/server communication

---

## 🚀 Features
- ✅ Real-time multi-user chat over TCP
- ✅ User registration and login
- ✅ Password hashing with SHA256
- ✅ Ngrok tunneling for remote connections
- ✅ Clean CLI-based interface

---

## 🛠️ Installation & Usage

### 1. Clone repository
```bash
git clone https://github.com/EvgeniaZimin/terminal-tcp-chat.git
cd terminal-tcp-chat

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the server
python server.py

### 4. Run the client
python client.py

📦 Requirements

Python 3.10+

pyngrok

hashlib

Dependencies are listed in requirements.txt.

🔒 Security Notes

This project was built for educational purposes.
Do not use it in production environments — authentication and encryption are minimal by design.

📜 License

Distributed under the MIT License.
