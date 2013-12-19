import webbrowser
import SimpleHTTPServer
import SocketServer
import urllib
from image_search import search, scrape
import json

class Server(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		operation = self.path[1:]
		length = int(self.headers.getheader('content-length'))        
		arg = self.rfile.read(length)
		if operation == "search":
			result = search(arg)
			#result = urllib.quote(result, "") #urllib.urlencode({"results":result})
			#result = "\n".join(map(urllib.urlencode,enumerate(search(arg))))
		elif operation == "scrape":
			result = scrape(arg)
		out =urllib.quote(json.dumps(result), "")
		self.wfile.write(out)


httpd = SocketServer.ThreadingTCPServer(("",0), Server)

PORT = httpd.socket.getsockname()[1]
image = "http://www.freefever.com/stock/rainbow-abstract-background-free.jpg"
webbrowser.open("http://127.0.0.1:%s/#%s" % (PORT, image))
print "Serving on port", PORT
httpd.serve_forever()
