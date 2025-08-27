# 🛰️ Terminal TCP Chat

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Multi-user **TCP chat** written in Python.  
Includes **user authentication**, **SHA256 password hashing**, and **ngrok tunneling** for public access.

---

## ✨ Features
- Real-time **multi-user chat** over TCP sockets
- **User registration & authentication** (SHA256 password hashing)
- **ngrok tunneling** — expose local server to the internet
- **Multi-threaded** server to handle multiple clients
- Simple **CLI interface** and graceful disconnects

---

## 🚀 Installation & Usage

### 1) Clone the repository
```bash
git clone https://github.com/EvgeniaZimin/terminal-tcp-chat.git
cd terminal-tcp-chat
```
###2) Create and activate virtual environment (recommended)
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\activate
```
###3) Install dependencies
```bash
pip install -r requirements.txt
```
###4) Authorize ngrok (one-time)
Get your token: https://dashboard.ngrok.com/get-started/your-authtoken

```bash
ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
```

###5) Run the server
```bash
python server.py
```
The server will ask for a TCP port (e.g., 54321).
It will then start an ngrok tcp endpoint and print a link like:
tcp://x.tcp.ngrok.io:12345

###6) Run the client and connect
```bash
python client.py
```
Paste the full link (e.g., tcp://x.tcp.ngrok.io:12345) and follow prompts to choose a name and register/sign in.

📂 Project Structure
```bash
terminal-tcp-chat/
├── server.py            # Chat server (TCP, threading, auth)
├── client.py            # Chat client (TCP CLI)
├── requirements.txt     # Dependencies (pyngrok)
├── LICENSE              # MIT License
└── README.md            # This file
```

🛠️ Tech Stack
Language: Python 3.10+

Stdlib: socket, threading, hashlib, select

External: pyngrok

Protocol: TCP/IP

Tunneling: ngrok (tcp)

Requirements
Python 3.10+

pyngrok (installed via requirements.txt)

🔐 Security Note
Educational project.
Do not use real credentials and do not run in production environments.

📄 License
This project is licensed under the MIT License.
