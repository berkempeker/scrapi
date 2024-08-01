from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
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

def handler(request):
    if request.method == 'GET':
        # Get the 'url' query parameter
        query_params = parse_qs(request.query_string)
        url = query_params.get('url', [''])[0]

        if url:
            result = get_urls_from_webpage(url)
            response = {"urls": result} if isinstance(result, list) else {"error": result}
        else:
            response = {"error": "No URL provided"}

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }
