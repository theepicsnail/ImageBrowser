import os
import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.escape
from tornado.options import define, options
import bs4
import urllib
import redis


tornado.options.define(
    "port", default=1922, help="run on the given port", type=int)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
pipe = r.pipeline()

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
        if r.exists(self.query):
            data = {}
            data[self.query] = r.get(self.query)
            d = tornado.escape.json_encode(tornado.escape.recursive_unicode(data[self.query]))
            return d
        else:
            url = "https://www.google.com/searchbyimage?image_url=" + self.query
            response = self._get_url_data(url)
            data = str(response.body)

            result_partition = data.split("Pages that include")
            if len(result_partition) != 2:
                return []
            data = result_partition[1]
            link_blobs = data.split('"r"><a href="')
            out = []
            for blob in link_blobs[1:]:
                out.append(blob.split('"')[0])
            return self.__get_images(out)

    # returns a list of image elements from a url
    def __get_images(self, urls):
        #dict holding url as the keys
        imgs = {}
        for url in urls:
            data = self._get_url_data(url)
            soup = bs4.BeautifulSoup(data.body)
            imgs[url] = []
            for img in soup.find_all("img", src=True):
                absurl = urllib.parse.urljoin(url, img['src'])
                imgs[url].append(absurl)
        pipe.set(self.query, imgs).expire(self.query, 864000).execute()
        return tornado.escape.json_encode(imgs)

    def _get_url_data(self, url):
        #check to see if url is in cache
        #if not in cache, crawl
        #if in cache, return cached url
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        http = tornado.httpclient.HTTPClient()
        req = tornado.httpclient.HTTPRequest(url, headers=headers)
        res = http.fetch(req)
        return res



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
