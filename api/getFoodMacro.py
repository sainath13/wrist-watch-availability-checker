# api/getFoodMacro.py
import json
from urllib import parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_path = parse.urlparse(self.path)
        query_params = parse.parse_qs(parsed_path.query)
        food = query_params.get('food', [None])[0]

        if not food:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Food query parameter is required.'}).encode('utf-8'))
            return

        # Return fixed macronutrient information
        response = {
            'Calories': 130,
            'Fat': '4g',
            'Carbs': '23g',
            'Protein': '2g'
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

