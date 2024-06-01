# api/data.py
import json
import datetime
from http.server import BaseHTTPRequestHandler
from textblob import TextBlob
from supabase import create_client, Client

url: str = "https://eugmxxtzlcdlrnosbowy.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1Z214eHR6bGNkbHJub3Nib3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwMDQzOTUsImV4cCI6MjAzMjU4MDM5NX0.TsfuVI_CDiXuiObg6GlToOlp37yGtWTLu3opXv_bB34"
supabase: Client = create_client(url, key)

journal_entries = []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        JournalEntry = data.get('JournalEntry')
        Mood = data.get('Mood')
        sentiment = TextBlob(JournalEntry).sentiment
        polarity = sentiment.polarity
        data, count = supabase.table('JournalEntries').insert({"mood": Mood, "mood_rating" : polarity, "journal_text" : JournalEntry }).execute()
        
        if not JournalEntry or not Mood:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'JournalEntry and Mood are required.'}).encode('utf-8'))
            return

        entry = {
            'id': len(journal_entries) + 1,
            'JournalEntry': JournalEntry,
            'Mood': Mood,
            'Polarity' : polarity,
            'createdAt': str(datetime.datetime.now())
        }

        journal_entries.append(entry)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Journal entry added.', 'entry': entry}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

