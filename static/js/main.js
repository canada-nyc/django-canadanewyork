CANADA = {};

// Configure Raven and install default handler to capture uncaught exceptions
$(document).ready(function () {
  Raven.config(CANADA.SENTRY_DSN, CANADA.RAVEN_CONFIG).install();

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
