# api/getSentiments.py
import json
from http.server import BaseHTTPRequestHandler
from textblob import TextBlob
from supabase import create_client, Client
url: str = "https://eugmxxtzlcdlrnosbowy.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1Z214eHR6bGNkbHJub3Nib3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwMDQzOTUsImV4cCI6MjAzMjU4MDM5NX0.TsfuVI_CDiXuiObg6GlToOlp37yGtWTLu3opXv_bB34"
supabase: Client = create_client(url, key)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            text = data.get('text')
        except (json.JSONDecodeError, KeyError):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid input. JSON with "text" is required.'}).encode('utf-8'))
            return
        
        if not text:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Text field is required.'}).encode('utf-8'))
            return
        
        sentiment = TextBlob(text).sentiment
        response = supabase.table("journal").select("*").execute()
        print(response)
        response = {
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            'rows' : response.data
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

