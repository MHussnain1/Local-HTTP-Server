import os
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer
import qrcode
from PIL import Image


def get_local_ip() -> str:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def validate_directory_path(path: str) -> str:
    if not path or not path.strip():
        raise ValueError("Please select a target folder path first.")

    clean_path = path.strip()
    if not os.path.exists(clean_path):
        raise ValueError(f"Path does not exist: {clean_path}")
    if not os.path.isdir(clean_path):
        raise ValueError(f"Selected path is not a valid directory: {clean_path}")

    return clean_path


def generate_qr_image(url: str) -> Image.Image:

    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(url)
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white").get_image()


class LocalFileServer:

    def __init__(self, port: int = 8000):
        self.port = port
        self.httpd = None

    def initialize_server(self, target_directory: str) -> str:

        valid_path = validate_directory_path(target_directory)

        class ScopedHTTPHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=valid_path, **kwargs)

        try:
            self.httpd = HTTPServer(("0.0.0.0", self.port), ScopedHTTPHandler)
        except OSError as e:
            raise RuntimeError(
                f"Port {self.port} is already in use or unavailable: {e}"
            )

        local_ip = get_local_ip()
        return f"http://{local_ip}:{self.port}"

    def serve_requests(self):

        if self.httpd:
            self.httpd.serve_forever()

    def stop_server(self):
        """Shuts down active HTTP server."""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None


if __name__ == "__main__":
    print("--- Independent Server Logic Test ---")
    test_dir = os.getcwd()
    print(f"Testing directory validation for: {test_dir}")
    try:
        validated = validate_directory_path(test_dir)
        print(f"Validation successful: {validated}")
        ip = get_local_ip()
        print(f"Local IP address resolved: {ip}")
        print("Module tests passed successfully.")
    except Exception as err:
        print(f"Test failed: {err}")
