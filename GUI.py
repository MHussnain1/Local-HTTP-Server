import threading
import customtkinter as ctk
from tkinter import filedialog
from Server_logic import LocalFileServer, generate_qr_image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FileServerUI(ctk.CTk):
    def __init__(self, port=8000):
        super().__init__()
        self.title("⚡ Local File Server")
        self.geometry("520x580")
        self.resizable(False, False)

        self.server_manager = LocalFileServer(port=port)
        self.server_thread = None

        self._build_ui()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self, text="⚡ Local File Server", font=("Segoe UI", 20, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Folder Selection Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(fill="x", padx=30, pady=10)

        self.path_entry = ctk.CTkEntry(
            self.path_frame, placeholder_text="No folder selected...", width=320
        )
        self.path_entry.pack(side="left", padx=(10, 5), pady=10)

        self.browse_btn = ctk.CTkButton(
            self.path_frame, text="Browse", width=80, command=self._handle_browse
        )
        self.browse_btn.pack(side="right", padx=(5, 10), pady=10)

        # Server Toggle Button
        self.toggle_btn = ctk.CTkButton(
            self,
            text="🚀 Start Server",
            font=("Segoe UI", 13, "bold"),
            fg_color="#2ba640",
            hover_color="#218332",
            height=40,
            command=self._handle_toggle_server,
        )
        self.toggle_btn.pack(fill="x", padx=30, pady=15)

        # Access Link & Status Card
        self.link_frame = ctk.CTkFrame(self, fg_color="#1e1e2e")
        self.link_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.status_label = ctk.CTkLabel(
            self.link_frame,
            text="Status: Stopped",
            font=("Segoe UI", 11, "bold"),
            text_color="#f38ba8",
        )
        self.status_label.pack(pady=(15, 2))

        self.url_entry = ctk.CTkEntry(
            self.link_frame, font=("Consolas", 12), justify="center", width=380
        )
        self.url_entry.pack(pady=(2, 10))

        # QR Code Image Label
        self.qr_label = ctk.CTkLabel(self.link_frame, text="", width=180, height=180)
        self.qr_label.pack(pady=10)

    def _handle_browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def _handle_toggle_server(self):
        if self.server_manager.httpd is None:
            raw_path = self.path_entry.get()

            try:
                # Core validation and initialization call
                access_url = self.server_manager.initialize_server(raw_path)
                
                # Start server on background thread
                self.server_thread = threading.Thread(
                    target=self.server_manager.serve_requests,
                    daemon=True
                )
                self.server_thread.start()

                # Generate & display QR Code
                pil_img = generate_qr_image(access_url)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 180))
                self.qr_label.configure(image=ctk_img)

                # Update UI state
                self.status_label.configure(
                    text="Status: Active & Serving Files", text_color="#a6e3a1"
                )
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, access_url)
                self.toggle_btn.configure(
                    text="🛑 Stop Server", fg_color="#e64553", hover_color="#d20f39"
                )

            except (ValueError, RuntimeError) as err:
                self.status_label.configure(text=f"Error: {err}", text_color="#f38ba8")

        else:
            # Stop server and update UI
            self.server_manager.stop_server()
            self.qr_label.configure(image=None)
            self.status_label.configure(text="Status: Stopped", text_color="#f38ba8")
            self.url_entry.delete(0, "end")
            self.toggle_btn.configure(
                text="🚀 Start Server", fg_color="#2ba640", hover_color="#218332"
            )