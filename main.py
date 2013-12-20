import SimpleHTTPServer
import SocketServer
import urllib
from image_search import search, scrape
import json

class Server(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        out = "[]"
        try:
            operation = self.path[1:]
            length = int(self.headers.getheader('content-length'))        
            arg = self.rfile.read(length)
            print operation, arg
            if operation == "search":
                result = search(arg)
            elif operation == "scrape":
                result = scrape(arg)
            out = urllib.quote(json.dumps(result), "")
        except: pass
        self.wfile.write(out)


PORT = 12347
httpd = SocketServer.ThreadingTCPServer(("",PORT), Server)

PORT = httpd.socket.getsockname()[1]
image = "http://www.freefever.com/stock/rainbow-abstract-background-free.jpg"
print "Serving at:", "http://127.0.0.1:%s/" % PORT
httpd.serve_forever()
