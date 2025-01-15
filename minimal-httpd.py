import http.server
import ssl
import socketserver
import base64

# Define the handler to serve files from the current directory
Handler = http.server.SimpleHTTPRequestHandler

# Minimal favicon
FAVICON = 'AAABAAEAEBAAAAAAIABSAAAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgCAAAAkJFoNgAA' \
          'ABlJREFUeJxjZGD4z0AKYCJJ9aiGUQ1DSgMAPjABH1olvcoAAAAASUVORK5CYII='

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(base64.b64decode(FAVICON))
        else:
            super().do_GET()

    def end_headers(self):
        # Add custom headers here
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'")
        self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        self.send_header('Permissions-Policy', "camera=(), microphone=(), geolocation=()")
        self.send_header('Referrer-Policy', 'no-referrer-when-downgrade')
        self.send_header('Strict-Transport-Security', "max-age=31536000; includeSubDomains; preload")
        self.send_header('X-Content-Type-Options', "nosniff")
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        # Call the superclass's end_headers method to send the headers
        super().end_headers()

def main(port=4443):
    # Create an instance of TCPServer with the specified handler
    with socketserver.TCPServer(("0.0.0.0", port), CustomHTTPRequestHandler) as httpd:
        print(f"Serving on port {port} with TLS")
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="/etc/pki/tls/certs/machine.pem",
                                keyfile="/etc/pki/tls/private/machine.key")

        # Wrap the server's socket with SSL
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        # Start the server
        httpd.serve_forever()

if __name__ == "__main__":
    main()
