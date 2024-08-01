from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import requests
from bs4 import BeautifulSoup

def get_urls_from_webpage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        return urls
    except Exception as e:
        return str(e)

def handle(url):
    if url:
        result = get_urls_from_webpage(url)
        return {"urls": result} if isinstance(result, list) else {"error": result}
    else:
        return {"error": "No URL provided"}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(self.path.split('?')[1]) if '?' in self.path else {}
        url = query.get('url', [''])[0]
        
        result = handle(url)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
        return
