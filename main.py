import webbrowser
import SimpleHTTPServer
import SocketServer
import urllib
from image_search import search, scrape
import json

class Server(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		print "do_post ---"
		operation = self.path[1:]
		print operation
		length = int(self.headers.getheader('content-length'))        
		arg = self.rfile.read(length)
		print arg
		if operation == "search":
			result = search(arg)
			#result = urllib.quote(result, "") #urllib.urlencode({"results":result})
			#result = "\n".join(map(urllib.urlencode,enumerate(search(arg))))
		elif operation == "scrape":
			result = scrape(arg)
		out =urllib.quote(json.dumps(result), "")
		print out
		self.wfile.write(out)
		print "---"



"""
works:
results=http%3A%2F%2Fwww.wallconvert.com%2Fconverted%2Frainbow-abstract-background-free-2384131-157138.html%0Ahttp%3A%2F%2Fwww.wallconvert.com%2Fconverted%2Fabstract-rainbow-background-132238.html%0Ahttp%3A%2F%2Fmoviecroft.com%2Frainbow-background-wallpaper.html%0Ahttp%3A%2F%2Fwww.freefever.com%2Fwallpaper%2F1920x1080%2Frainbow-abstract-background-free-28791.html%0Ahttp%3A%2F%2Fhdw.eweb4.com%2Fout%2F737172.html

results=http%3A%2F%2Fwww.wallconvert.com%2Fconverted%2Frainbow-abstract-background-free-2384131-157138.html%0Ahttp%3A%2F%2Fwww.wallconvert.com%2Fconverted%2Fabstract-rainbow-background-132238.html%0Ahttp%3A%2F%2Fmoviecroft.com%2Frainbow-background-wallpaper.html%0Ahttp%3A%2F%2Fwww.freefever.com%2Fwallpaper%2F1920x1080%2Frainbow-abstract-background-free-28791.html%0Ahttp%3A%2F%2Fhdw.eweb4.com%2Fout%2F737172.html



"""

httpd = SocketServer.ThreadingTCPServer(("",0), Server)

PORT = httpd.socket.getsockname()[1]
image = "http://www.freefever.com/stock/rainbow-abstract-background-free.jpg"
webbrowser.open("http://127.0.0.1:%s/#%s" % (PORT, image))
httpd.serve_forever()
