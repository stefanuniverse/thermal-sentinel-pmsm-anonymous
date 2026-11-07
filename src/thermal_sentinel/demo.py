"""Loopback-only local demo. No raw data, weights or local directories served."""
import argparse
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit
from pathlib import Path
import json
from .data import ROOT

WEB=Path(__file__).resolve().parent/'web/index.html'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        allowed={'/':WEB,'/index.html':WEB,
            '/results/experiment.json':ROOT/'results/experiment.json',
            '/results/replay.json':ROOT/'results/replay.json',
            '/results/experiment-ridge.json':ROOT/'results/experiment-ridge.json',
            '/results/replay-ridge.json':ROOT/'results/replay-ridge.json'}
        target=allowed.get(path)
        if target is None or not target.is_file():
            self.send_error(404);return
        blob=target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8' if target==WEB else 'application/json')
        self.send_header('Content-Length',str(len(blob)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers();self.wfile.write(blob)
    def log_message(self,*args):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=4382);args=ap.parse_args()
    print(f'Research-only local demo: http://127.0.0.1:{args.port}/',flush=True)
    with ThreadingHTTPServer(('127.0.0.1',args.port),Handler) as server:server.serve_forever()

if __name__=='__main__':main()
