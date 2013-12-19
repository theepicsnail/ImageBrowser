
function search_input_image() {
  var image_url = $("#img_input").val()
  console.log(image_url)
  $("#out").empty();
  $.post("search", image_url, on_search_results);
}
function on_search_results(data) { 
  console.log(arguments)
  console.log("search results: ", unescape(data))
  var urls = JSON.parse(unescape(data))
  for (var key in urls) {
    console.log(urls,key,urls[key])
    $.post("scrape", urls[key], on_scrape_results);
  }
}
function on_scrape_results(data) {
  var urls = JSON.parse(unescape(data))
  for (var key in urls) {
    append_image(urls[key])
  }
}

function append_image(path) {

$('<img />').attr({
  src:path
  //width:'100',
  //height:'100'
}).click(function(e){
  $("#img_input").val(path);
  search_input_image();
})
.appendTo($('<a />').attr({
  href:'#' + path
}).appendTo($('#out')));

/*
    $('<img src="'+ path +'">').load(function() {
	var me =  $(this);
	me = me.wrap("<a href='"+path+"'></a>");
	me.appendTo($("body"));
      //$(this).appendTo($("body"));
	//	.width(width).height(height)
    });
*/
    //$("a").attr("href", "#" + image_url).append(
}

$(function() {
  $("#img_input").keypress(function (e) {
    if (e.which == 13) {
      search_input_image()
    }
  });
  // Get the image url from the location's hash
  var image_url = location.hash.substring(1);
  if (image_url !== "") {
    $("#img_input").val(image_url)
    search_input_image()
  }
  // Search by that url
  // For each of the returned urls:
  //   Get that page
  //   Parse images from that page
  //   Add images to some list of images
  // For each image in the list of images
  //   Add an image/link that takes the user back here
  //   ... with the images absolute url in the hash 
});
