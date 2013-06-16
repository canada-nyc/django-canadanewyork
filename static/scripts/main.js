CANADA = {};

$(document).ready(function () {
  // Initialize the lightbox
  var lightbox = new CANADA.Lightbox();
  $('.gallery').on('click', function () {
    var id = $(this).attr('id');
    lightbox.show(id);
  });

  $('.open-gallery').on('click', function () {
    $($(this).attr('href')).click();
  });

});
