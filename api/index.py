from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Basic HTML with a link to test the ingest endpoint
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Opacity Ingest Test</title>
        </head>
        <body>
            <h1>Opacity Ingest Test</h1>
            <p>This is a simple test page for the ingest endpoint.</p>
            <a href="/api/ingests">Go to Ingest Endpoint</a>
        </body>
        </html>
        """

        # Send HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode())
