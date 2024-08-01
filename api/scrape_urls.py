from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json

def get_urls_from_webpage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        return urls
    except Exception as e:
        return f"An error occurred: {e}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Get the 'url' query parameter
        from urllib.parse import urlparse, parse_qs
        query_components = parse_qs(urlparse(self.path).query)
        url = query_components.get('url', [''])[0]

        if url:
            result = get_urls_from_webpage(url)
            response = json.dumps({"urls": result} if isinstance(result, list) else {"error": result})
        else:
            response = json.dumps({"error": "No URL provided"})

        self.wfile.write(response.encode())
        return
