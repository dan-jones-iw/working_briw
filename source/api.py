from source.db import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class PersonHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        people = get_all_people()

        jd = json.dumps(people)
        self.wfile.write(jd.encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))

        save_person(data["name"], data["age"], data["favourite_drink_id"])

        self.send_response(200)


def run(port=8008, server_class=HTTPServer, handler_class=PersonHandler):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print("Starting running..")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
