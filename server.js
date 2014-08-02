var Promise = require('es6-promise').Promise;
var resolve = require('url').resolve;
var express = require('express');
var request = require('request');
var cheerio = require('cheerio');
var app     = express();
var user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 ' +
              '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17';

function get(get_url) {
  return new Promise(function(ret, thr) {
    request({ url:get_url, headers: { 'User-Agent': user_agent }},
      function (error, response, html) {
        if(error) thr(error);
        else ret(html);
      });
  });
}

app.use(express.static(__dirname + "/public"));
app.get('/', function(req, res){res.sendfile('index.html');});
app.get('/search', function(req, res){
  var search_url = req.query.url;
  console.log("Search:",search_url);
  if(!search_url) {
    res.send("no url provided. /search?url=http://...");
    return;
  }

  get("https://www.google.com/searchbyimage?image_url=" + search_url)
  .then(function(html) {
    res.send({'urls':
      cheerio.load(html)('.r a') // links
      .map(function(idx, page) { // without ?... stuff
        return page.attribs.href.split("?")[0];
      })
      .toArray() // as and array
      .filter(function(val, idx, slf) { // of unique links
        return idx === slf.indexOf(val);
      })
    });
  })
  .catch(function(error) {
      res.send({'urls': [],'error':error});
  });
});

app.get('/scrape', function(req, res) {
  var scrape_url = req.query.url;
  console.log("Scrape:", scrape_url);
  if(!scrape_url) {
    res.send("no url provided. /scrape?url=http://...");
    return;
  }
  get(scrape_url)
  .then(function(html) {
    res.send({'urls':
      cheerio.load(html)('img')
      .map(function(idx, a){
        return resolve(scrape_url,a.attribs.src);
      })
      .toArray()
    });
  })
  .catch(function(error) {
    res.send({'urls': [], 'error': error});
  });
});
var port = process.env.PORT || 1234;
app.listen(port);
console.log('Magic happens on port ' + port);
exports = module.exports = app;
