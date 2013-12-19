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
import bs4
import urllib

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
            self.http = tornado.httpclient.HTTPClient()
            self.headers = {}
            self.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            urls = self.__search()
            results = self.__get_images(urls)
            self.render("index.html", results=results)
        self.render("index.html", results=False)

    def __search(self):
        cache_file = "cache/%s.html" % abs(hash(self.query))
        if os.path.exists(cache_file):
            data = file(cache_file).read().decode('utf8')
        else:
            req = tornado.httpclient.HTTPRequest("https://www.google.com/searchbyimage?image_url=" + self.query, headers=self.headers)
            response = self.http.fetch(req)
            data = str(response.body)
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
    def __get_images(self, urls):
        #dict holding url as the keys
        imgs = {}
        for url in urls:
            req = tornado.httpclient.HTTPRequest(url, headers=self.headers)
            response = self.http.fetch(req)
            soup = bs4.BeautifulSoup(response.body)
            imgs[url] = []
            for img in soup.find_all("img", src=True):
                imgs[url].append(urllib.parse.urljoin(url, img['src']))
        print(imgs)
        return imgs


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
