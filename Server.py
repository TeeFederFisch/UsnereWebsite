from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHttpHandler(SimpleHTTPRequestHandler):
    def end_headers (self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)

def run(server_class=HTTPServer, handler_class=MyHttpHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()