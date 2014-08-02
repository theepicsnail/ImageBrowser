function rpc(method, url, callback) {
  // rpc('search', img url, cb); -> cb({urls:list of http urls})
  // rpc('scrape', http url, cb); -> cb({urls:list of img urls})
  var xhr = new XMLHttpRequest();
  xhr.open("get", "/" + method + "?url=" + url, true);
  xhr.onreadystatechange=function() {
    if(xhr.readyState !== 4) {return;}
    if(xhr.status !== 200) {return;}
    callback(JSON.parse(xhr.responseText));
  };
  xhr.send();
}

function clear(id) {
  var element = document.getElementById(id);
  while(element.childNodes.length > 0) {
    element.removeChild(element.childNodes[0]);
  }
}

function addUrl(url) {
  var element = document.createElement('li');
  element.textContent = url;
  document.getElementById('urls').appendChild(element);
}
function addImg(url) {
  var img = document.createElement('img');
  img.onerror = img.onload = function(){
    loaded_images ++;
    update_scrape_status();
  };
  img.src = url;
  var link = document.createElement('a');
  link.appendChild(img);
  link.href="?" + url;
  document.getElementById('imgs').appendChild(link);
}

function startSearch(img_url) {
  clear('imgs');
  clear('urls');
  set_status("Performing search");
  rpc('search', img_url, handle_search_results);
}

function handle_search_results(results) {
  var idx;
  if(results.error) {
    console.log(results.error);
  }

  if(results.urls.length === 0) {
    set_status("No results found.");
  } else {
    set_status("Found " + results.urls.length + " page(s). Starting scrape");
    total_pages = results.urls.length;
  }

  for(idx = 0; idx < results.urls.length ; idx ++) {
    addUrl(results.urls[idx]);
    rpc('scrape', results.urls[idx], handle_scrape_results);
  }
}

var loaded_images = 0, loaded_pages = 0;
var total_images = 0, total_pages =0;
function update_scrape_status() {
  set_status("Pages: ["+loaded_pages+" of "+total_pages+"] || Images: [" + loaded_images + " of " + total_images + "]");
}
function handle_scrape_results(results) {
  loaded_pages ++;
  var idx;
  if(results.error) {
    set_status(results.error);
    console.log(results.error);
  }

  total_images += results.urls.length;
  update_scrape_status();
  for(idx = 0; idx < results.urls.length ; idx ++) {
    addImg(results.urls[idx]);
  }
}

function set_status(str) {
  document.getElementById('status').innerHTML = str;
}

window.onload = function() {
  var img_url = location.search.substr(1);
  if (img_url.search('url=') === 0) { // Web form submission
    img_url = img_url.substr(4);
  }
  console.log("image url detected:", img_url);
  if (img_url) {
    startSearch(img_url);
  }
};
