CANADA = {};

$(document).ready(function () {
  if ("onhashchange" in window) {
    var lightbox = new CANADA.Lightbox(),
        _show = lightbox.show,
        _close = lightbox.close;

    lightbox.show = function (galleryId) {
      window.location.hash = galleryId;
      _show.call(this, galleryId);
    };
    lightbox.close = function () {
      window.location.hash = '';
      _close.call(this);
    };

    window.onhashchange = function () {
      var hash = window.location.hash;
      if (hash === '') {
        lightbox.close();
      } else {
        lightbox.show(hash.slice(1));
      }
    };
  }

});
