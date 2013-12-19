import os
import re
import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import unicodedata
import urllib3
import bs4
import urllib
import requests

from tornado.options import define, options

tornado.options.define(
    "port", default=1922, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            #/user, /matches  are for the api
            (r"/", IndexHandler),
            # (r"/answers", AnswerHandler),
            # (r"/bakasubo", ScrapeHandler),

        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            autoescape=None
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.query = self.get_argument("query", default=None)
        if self.query:
            results = self.__search()
            self.render("index.html", results=results)
        self.render("index.html", results=False)

    def __search(self):
        cache_file = "cache/%s.html" % abs(hash(self.query))
        if os.path.exists(cache_file):
            data = file(cache_file).read().decode('utf8')
        else:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = "https://www.google.com/searchbyimage?image_url=" + self.query
            response = requests.get(req, headers=headers)
            data = response.text
            file = open(cache_file, "wb").write(data.encode('utf8'))

        result_partition = data.split("Pages that include")
        if len(result_partition) != 2:
            return []
        data = result_partition[1]
        link_blobs = data.split('"r"><a href="')
        out = []
        for blob in link_blobs[1:]:
            out.append(blob.split('"')[0])
        return out

    # returns a list of image elements from a url
    def __get_images(self, url):
        http = urllib3.PoolManager()
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        response = http.request("GET", url, headers=headers)
        soup = bs4.BeautifulSoup(response.data)
        img_urls = []
        for img in soup.find_all("img", src=True):
            img_urls.append(urllib.parse.urljoin(url, img['src']))
        return img_urls


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
