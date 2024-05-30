# api/getSentiments.py
import json
from http.server import BaseHTTPRequestHandler
from textblob import TextBlob
import sqlite3


conn = sqlite3.connect('example.db')
cursor = conn.cursor()


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
        
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        response = {
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity
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

