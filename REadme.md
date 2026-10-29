# ⚡ Local File Server Desktop Application

A lightweight, modern desktop application built with Python that allows you to instantly host and share files or entire folders from your PC over a Local Area Network (LAN). Connected devices on the same Wi-Fi network can view and download shared files using a generated web URL or by scanning an automatically generated QR code.

---

## 🚀 Use Cases

* **Wireless Phone & Tablet File Transfers:** Share documents, photos, or APKs directly to your mobile device without plugging in USB cables or uploading sensitive data to third-party cloud services.
* **Local Team Asset Sharing:** Share large project folders, software builds, or design assets instantly with team members on the same office or home Wi-Fi network.
* **Cross-Platform Media Streaming:** Play video or audio files directly inside a mobile browser without copying them over to local mobile storage first.
* **Offline Network Sharing:** Serve files locally even without an active internet connection (requires only a local router or hotspot connection).

---

## 📋 Requirements & Prerequisites

* **Python Version:** Python 3.8 or higher.
* **Operating System:** Windows 10/11, macOS, or Linux.
* **Network:** An active Local Area Network (Wi-Fi router or mobile hotspot) shared between the host PC and client devices.

---

## 📦 Dependencies

### Standard Library (Pre-installed)
* `os` — Directory checking and path operations.
* `socket` — System network interface and local IP detection.
* `threading` — Asynchronous background task execution.
* `http.server` — Embedded HTTP server engine.
* `tkinter` — Native file picker dialogs.

### Third-Party Libraries
Install all third-party dependencies using `pip`:

```bash
pip install customtkinter qrcode pillow
```

| Package | Version | Purpose |
| :--- | :--- | :--- |
| **`customtkinter`** | `^5.2.0` | Provides a modern, dark-themed GUI widget system. |
| **`qrcode`** | `^7.4.2` | Generates QR code matrix data from URLs. |
| **`pillow`** | `^10.0.0` | Handles image manipulation and rendering for CustomTkinter image widgets. |

---

## 📂 Project Structure

```text
file_server_project/
│
├── server_logic.py   # Core business logic, validation, and network server engine
├── gui.py            # User interface layer (CustomTkinter GUI)
├── main.py           # Application entry point
└── README.md         # Documentation
```

---

## ⚙️ Installation & Running

1. **Clone or Download** the project files into a folder on your system.
2. **Install Dependencies:**
   ```bash
   pip install customtkinter qrcode pillow
   ```
3. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 🛠️ Design Principles Followed

1. **One function = One responsibility:** Functions are dedicated strictly to single tasks (e.g., path validation, IP resolution, QR generation).
2. **Input Validation:** Input folder paths are validated for existence and directory status before initializing socket listeners.
3. **Decoupled Architecture:** Business logic (`server_logic.py`) is completely separated from the presentation layer (`gui.py`).
4. **Error Handling:** Graceful error handling for missing directories, occupied ports (`OSError`), and thread execution.
5. **Independent Testing:** The `server_logic.py` module includes a runnable unit check under `if __name__ == "__main__":` to test core functions without launching the UI.
6. **Main Entry Point:** System invocation and main event loop start in `main.py`.