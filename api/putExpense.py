# api/data.py
import json
import datetime
from http.server import BaseHTTPRequestHandler
from textblob import TextBlob
from supabase import create_client, Client

url: str = "https://eugmxxtzlcdlrnosbowy.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1Z214eHR6bGNkbHJub3Nib3d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwMDQzOTUsImV4cCI6MjAzMjU4MDM5NX0.TsfuVI_CDiXuiObg6GlToOlp37yGtWTLu3opXv_bB34"
supabase: Client = create_client(url, key)

expence_entries = []
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        category = data.get('category')
        money_spent = data.get('money_spent')
        item = data.get('expense_item')
        
        data, count = supabase.table('BudgetEntries').insert({"category": category, "amount" : money_spent, "item" : item }).execute()
        
        if not category or not money_spent:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Category and amount are required.'}).encode('utf-8'))
            return

        entry = {
            'id': len(expence_entries) + 1,
            'category': category,
            'money_spent': money_spent,
            'expense_item' : item,
            'createdAt': str(datetime.datetime.now())
        }

        expence_entries.append(entry)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Expense added to db.', 'entry': entry}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

