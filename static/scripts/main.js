CANADA = {};

$(document).ready(function () {
  // Initialize the lightbox
  CANADA.lightbox = new CANADA.Lightbox();
  $('.gallery').on('click', function () {
    var id = $(this).attr('id');
    window.location.hash = id;
    CANADA.lightbox.show(id);
  });

  $('.open-gallery').on('click', function () {
    $($(this).attr('href')).click();
  });

});
