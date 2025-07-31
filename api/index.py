from http.server import BaseHTTPRequestHandler
import json
import requests
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Prepare request to the app-links/create endpoint
        api_url = f"{os.getenv('API_URL')}/app-links/create"
        api_key = os.getenv('OPACITY_API_KEY')

        # Payload with your provided templateId
        payload = {
            "apiKey": api_key,
            "templateId": "c8f98b35-bf1b-4af7-9a83-527428f0e185",
            "metadata": {
                "maxValue": "12345"
            }
        }

        # Make POST request
        try:
            resp = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
            resp_json = resp.json()
        except Exception as e:
            resp_json = {"error": str(e)}

        # Pretty-print JSON
        pretty_json = json.dumps(resp_json, indent=2)

        # Extract URL from nested status.url if present
        link_url = None
        if isinstance(resp_json, dict) and "status" in resp_json:
            status_data = resp_json.get("status", {})
            if isinstance(status_data, dict):
                link_url = status_data.get("url")

        # Fallback link if not found
        if not link_url:
            link_url = "/api/ingests"

        # Build HTML
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
            <p>Response from <code>/app-links/create</code>:</p>
            <pre>{pretty_json}</pre>
            <a href="{link_url}">Open Generated Link</a>
        </body>
        </html>
        """

        # Send HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content)
