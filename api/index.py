from http.server import BaseHTTPRequestHandler
import requests

url = "https://www.hmtwatches.in/product_details?id=eyJpdiI6Ii9weGRHYk02Qmh6WGViYWFjVWY5ZEE9PSIsInZhbHVlIjoiS3BXOVlQM1RnblBWdkpHcEZFeXMxQT09IiwibWFjIjoiZTc4OWQ3YzMzZjQ1ZTJkOGI5NWZhNTA2ZTc2Mzc5NWI2YmJiOWYwOTM5NTBkMWE1MDdmOTcxYTI2MjliNTcwZSIsInRhZyI6IiJ9"

def check_availability(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "Out Of Stock" not in response.text:
                return "The watch is available!"
            else:
                return "The watch is out of stock."
        else:
            return "Failed to fetch webpage. Status code:" + response.status_code
    except Exception as e:
        return "An error occurred:"+ str(e)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        strToPrint = check_availability(url)
        self.wfile.write(strToPrint.encode('utf-8'))
        return
