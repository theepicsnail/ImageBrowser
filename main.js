$(function() {
  // Get the image url from the location's hash
  var image_url = location.hash.substring(1);
  console.log("Image url:", image_url);

  // Search by that url
  // For each of the returned urls:
  //   Get that page
  //   Parse images from that page
  //   Add images to some list of images
  // For each image in the list of images
  //   Add an image/link that takes the user back here
  //   ... with the images absolute url in the hash 
});