from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = open("index.html").read()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html, "utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 80), SimpleHandler)
    print("Server running on http://0.0.0.0:80")
    server.serve_forever()
