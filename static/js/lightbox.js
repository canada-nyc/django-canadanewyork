(function () {

var slice = Array.prototype.slice;
var bind = function (fn, scope, args) {
  args = slice.call(arguments, 2);
  return function () {
    fn.apply(scope, args.concat(slice.call(arguments, 0)));
  };
};

var KEY_LEFT  = 37,
    KEY_RIGHT = 39,
    KEY_ESC   = 27;

CANADA.Lightbox = function () {
  $('body').append(CANADA.render('lightbox'));

  $('.lightbox .close').on('click', bind(this.close, this));
  $('.lightbox .next') .on('click', bind(this.next, this));
  $('.lightbox .prev') .on('click', bind(this.prev, this));

  $(document).on('keydown', bind(this.interpretKeyboardEvent, this));
  $(window).on('resize', bind(this.frameSizeDidChange, this));
};

CANADA.Lightbox.prototype = {

  isShowing: false,

  interpretKeyboardEvent: function (ev) {
    switch (ev.which) {
    case KEY_LEFT:
      this.prev();
      break;
    case KEY_RIGHT:
      this.next();
      break;
    case KEY_ESC:
      this.close();
      break;
    }
  },

  prev: function () {
    if (this.isShowing) {
      this.swipe.prev();
    }
  },

  next: function () {
    if (this.isShowing) {
      this.swipe.next();
    }
  },

  close: function () {
    if (this.isShowing) {
      this.isShowing = false;
      $('.lightbox').fadeOut(bind(this.closed, this));
    }
  },

  closed: function () {
    if (this.swipe) this.swipe.kill();
    $(this.element).remove();
    this.element = null;
    this.model = null;
  },

  show: function (galleryId) {
    var gallery = CANADA.store.find('gallery', galleryId);

    $('.lightbox').append(CANADA.render('gallery', gallery));

    this.model   = gallery;
    this.element = $('#gallery-' + galleryId)[0];
    if (gallery.photos.length == 1) {
      $('.lightbox').find('.next, .prev').hide();
    } else {
      $('.lightbox').find('.next, .prev').show();
    }

    $('.lightbox').fadeIn(bind(this.shown, this));

    var photos = gallery.photos,
        photo, image,
        $img, $figure;

    // Show spinners until the image has loaded
    for (var i = 0, len = photos.length; i < len; i++) {
      photo = photos[i];
      image = photo.sizes.large || photo.sizes.thumb;
      $img = $('#photo-' + photo.id);
      $img.hide();
      $figure = $img.parent();
      $figure.prepend('<div class="throbber" style="width: ' + image.width + 'px; height: ' + image.height + 'px"></div>');
      $img.imagesLoaded(bind(this.imageLoaded, this, photo));

      // Scale the photos when we first show the lightbox
      this.scalePhotoToFit(photo);
    }
  },

  shown: function () {
    this.swipe = Swipe(this.element);
    this.isShowing = true;
  },

  imageLoaded: function (photo) {
    var $img = $('#photo-' + photo.id),
        $figure = $img.parent();

    $figure.find('.throbber').hide();
    $img.fadeIn();
  },

  frameSizeDidChange: function () {
    // Only retile if we're showing content
    if (this.element) {

      // Scale all of the photos in this gallery to fit
      // the screen properly
      var photos = this.model.photos;
      for (var i = 0, len = photos.length; i < len; i++) {
        this.scalePhotoToFit(photos[i]);
      }
    }
  },

  scalePhotoToFit: function (photo) {
    var image    = photo.sizes.large || photo.sizes.thumb,
        $img     = $('#photo-' + photo.id),
        $figure  = $img.parent(),
        $caption = $figure.find('aside');

    // Resize the photo so the caption and photo are both
    // completely visible.
    var availableHeight = $(window).height() -
                          $img.offset().top -
                          $caption.outerHeight(),
        scale = 1;

    // Scale down the image
    if (image.height > availableHeight) {
      scale = availableHeight / image.height;
    }

    // Scale and center the image
    if (scale < 1) {
      $img.css({
        height:     (scale * image.height)    + "px",
        marginLeft: (scale * image.width / 2) + "px"
      });

    // Remove styling to let the browser do it's thing
    } else {
      $img.removeAttr('style');
    }
  }

};

}());
