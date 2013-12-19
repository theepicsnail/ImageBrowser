import os
import urllib2
import urlparse

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent',  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17")]

CACHE_DIR = "cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_url_data(url):
    cache_file = os.path.join(CACHE_DIR, "C%s.html" % hash(url))
    if os.path.exists(cache_file):
	print "Found in cache"
        data = file(cache_file).read()
    else:
        headers = {}
        data = opener.open(url).read()
	f = file(cache_file, "w")
	f.write(data)
	f.close()
    return data

def search(image_url):
    data = get_url_data("https://www.google.com/searchbyimage?image_url=" + image_url)
    result_partition = data.split("Pages that include")
    if len(result_partition) != 2:
	print "Pages that include was not found"
        return []
    data = result_partition[1]
    link_blobs = data.split('"r"><a href="')
    out = []
    print "Link blob partitions:", len(link_blobs)
    for blob in link_blobs[1:]:
        out.append(blob.split('"')[0])
    print "Returning"
    print out
    return out

def scrape(url):
    data = get_url_data(url)
    img_tags = data.split("img src=")[1:]
    img_srcs= []
    for imgtag in img_tags:
        delim = imgtag[0]
        img_path = imgtag.split(delim)[1]
        img_src = urlparse.urljoin(url, img_path)
        img_srcs.append(img_src)
    return img_srcs
if __name__ == "__main__":
    image_url = "http://i0.kym-cdn.com/photos/images/original/000/000/130/disaster-girl.jpg"
    for url in search(image_url):
        print url

