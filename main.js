function perform_search(image_url) {
    $("#img_input").val(image_url);
    search_input_image();
}
function search_input_image() {
  var image_url = $("#img_input").val();
  console.log(image_url);
  $("#out").empty();
  $.post("search", image_url, on_search_results);
}

//var incoming_results = 0;
function on_search_results(data) { 
  console.log(arguments);
  console.log("search results: ", unescape(data));
  var urls = JSON.parse(unescape(data));

  //incoming_results = urls.length;
  for (var key in urls) {
    console.log(key,urls[key]);
    $.post("scrape", urls[key], on_scrape_results);
  }
}
function on_scrape_results(data) {
  var urls = JSON.parse(unescape(data));
  console.log("result:", urls.length)
  for (var key in urls) {
    load_image(urls[key]);
  }
   
  /*incoming_results -= 1;
  if (incoming_results === 0) {
    console.log("Masonrying")
    $container = $('#out');
    $container.imagesLoaded(function(){
      $container.masonry({
        itemSelector: '.item'
      });
    });
  }*/

}


var unique_image_id = 0;
function load_image(image_url) {

  //Make this image unique
  var image_id = "img" + unique_image_id;
  unique_image_id += 1;

  var container = $("<div>").attr({
    'class':'item', 
    'id':unique_image_id
  });

  var img = $('<img />').attr({'src':image_url});
  img.one('load', function() {
    console.log("loaded ", image_url);
    //Upon loading the image, insert it where it goes
    //var insertion_point = insert_image($(this).width,  unique_image_id);
    $("#out").append(container);
    var divs = $("#out").children();
    divs.sort(function(a,b){
      return $(b).width() - $(a).width();
    });
    $("#out").append(divs);
  });
  img.each(function() {
    //Ensure we fire 'load' when the image has loaded
    if(this.complete) $(this).trigger('load'); 
  });
  img.click(function(e){
    //When the image is clicked, search using that image url
    perform_search(image_url);

  });
  img.appendTo(container);

}


var imageWidths = [[-1, "#out"]]; // list of [image width, id]
var next_id = 1;
function find_appending_target(width, id) {
  //Return the element id if the element that should be 
  //right before the passed in element
  var idx = imageWidths.length -1;
  while(imageWidths[idx][0] > width) idx -= 1; //This could be quicker but O(n)'s fine
  return imageWidths[idx][1];
}

function append_image(path) {

/*$('<div>').css({
  'content': 'url(' + path +')',
  }).attr({
  'class': 'item',
  }).appendTo($("#out"));
  */
$('<img />').attr({
  src:path
  //width:'100',
  //height:'100'
}).click(function(e){
  $("#img_input").val(path);
  search_input_image();
})
.appendTo($('<div>').attr({
  'class':'item',
//  href:'#' + path
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
      perform_search($("#img_input").val()); // Does this value exist in 'e'?
    }
  });
  // Get the image url from the location's hash
  var image_url = location.hash.substring(1);
  if (image_url !== "") {
    perform_search(image_url);
  }
});
