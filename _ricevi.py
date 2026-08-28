# Ricevitore: scrive su file quello che la pagina gli manda in POST.
# Serve perche' un WAV di due megabyte non puo' passare dal ponte JavaScript.
import os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

OUT = os.path.dirname(os.path.abspath(__file__))

class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        dati = self.rfile.read(n)
        nome = os.path.basename(self.path.strip('/')) or 'audio.wav'
        with open(os.path.join(OUT, nome), 'wb') as f:
            f.write(dati)
        print('scritto', nome, len(dati), 'byte', flush=True)
        self.send_response(200); self.cors(); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass

HTTPServer(('127.0.0.1', 8159), H).serve_forever()
