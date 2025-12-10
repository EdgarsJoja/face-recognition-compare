import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

import cv2
import numpy as np


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html = open("index.html").read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/process":
            try:
                # Parse multipart form data
                content_type = self.headers["content-type"]
                if not content_type:
                    self.send_error(400, "No content-type header")
                    return

                # Parse the form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        "REQUEST_METHOD": "POST",
                        "CONTENT_TYPE": content_type,
                    },
                )

                if "frame" not in form:
                    self.send_error(400, "No frame in request")
                    return

                # Read the uploaded image
                file_item = form["frame"]
                img_bytes = file_item.file.read()

                # Decode image
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if img is None:
                    self.send_error(400, "Invalid image")
                    return

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

                # Encode back to JPEG
                _, buffer = cv2.imencode(
                    ".jpg", processed, [cv2.IMWRITE_JPEG_QUALITY, 85]
                )

                # Send response
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.send_header("Content-Length", str(len(buffer)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(buffer.tobytes())

            except Exception as e:
                print(f"Error processing frame: {e}")
                self.send_error(500, f"Processing error: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 80), SimpleHandler)
    print("Server running on http://0.0.0.0:80")
    print("Endpoints:")
    print("  GET  /          - Serve HTML page")
    print("  POST /process   - Process video frames")
    server.serve_forever()
