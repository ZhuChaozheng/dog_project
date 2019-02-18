#!/usr/bin/python3


from http.server import HTTPServer, CGIHTTPRequestHandler

port = 8000

httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()
