import os
import requests
import urllib3
import bs4
import urllib


def search(image_url):
    cache_file = "cache/%s.html" % abs(hash(image_url))
    if os.path.exists(cache_file):
        data = file(cache_file).read().decode('utf8')
    else:
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        response = requests.get(
            "https://www.google.com/searchbyimage?image_url=" + image_url, headers=headers)
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
def get_images(url):
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



if __name__ == "__main__":
    image_url = "http://i0.kym-cdn.com/photos/images/original/000/000/130/disaster-girl.jpg"
    for url in search(image_url):
        print(get_images(url))
