from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Prepare request to the app-links/create endpoint
        api_url = f"{os.getenv('API_URL')}/app-links/create"
        api_key = os.getenv('API_KEY')
        

        # Use your provided templateId
        payload = {
            "apiKey": api_key,
            "templateId": "c8f98b35-bf1b-4af7-9a83-527428f0e185",
            "metadata": {
                "maxValue": "12345"
            }
        }

        # Make POST request to Opacity API
        try:
            resp = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
            resp_json = resp.json()
        except Exception as e:
            resp_json = {"error": str(e)}

        # Pretty-print JSON response
        pretty_json = json.dumps(resp_json, indent=2)

        # Build HTML page
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Opacity Ingest Test</title>
            <style>
                body {{ font-family: monospace; padding: 20px; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
                a {{ display: inline-block; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Opacity Ingest Test</h1>
            <p>{api_key}</p>
            <p>{api_url}</p>
            <p>Response from <code>/app-links/create</code>:</p>
            <pre>{pretty_json}</pre>
            <a href="/api/ingests">Go to Ingest Endpoint</a>
        </body>
        </html>
        """

        # Send HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode())
