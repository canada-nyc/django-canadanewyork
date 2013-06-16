(function () {

var slice = Array.prototype.slice;
var bind = function (fn, scope, args) {
  args = slice.call(arguments, 2);
  return function () {
    fn.apply(scope, args.concat(slice.call(arguments, 0)));
  };
};

var hasTouchCapabilities = ('ontouchstart' in window) || window.DocumentTouch && document instanceof DocumentTouch;

if (hasTouchCapabilities) {
  $('body').addClass('touch');
}

// Stashed CSS when we were altering the height of the image
var stashedCSS = {};

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
    }
  },

  shown: function () {
    this.swipe = Swipe(this.element);
    this.isShowing = true;

    // Scale the photos when we first show the lightbox
    // only **after** Swipe is initialized
    this.frameSizeDidChange();
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
        $caption = $figure.find('aside'),
        paddingTop = parseInt($figure.css('marginTop'), 10) +
                     parseInt($figure.css('paddingTop'), 10);

    // Stash the style
    if (!stashedCSS[photo.id]) {
      stashedCSS[photo.id] = $img.attr('style');
    }

    // Resize the photo so the caption and photo are both
    // completely visible.
    var availableHeight = $(window).height() -
                          paddingTop * 2 -
                          $caption.outerHeight(),
        availableWidth  = $figure.width(),
        dimensions = {},
        scale = 1;

    // Get the current scale
    if (image.width > availableWidth) {
      scale = availableWidth / image.width;
    }
    dimensions.width  = image.width  * scale;
    dimensions.height = image.height * scale;

    // Scale down the image (more)
    if (dimensions.height > availableHeight) {
      scale = (availableHeight / dimensions.height);

    // Ignore our initial scale- the browser's doing all the work
    } else {
      scale = 1;
    }

    // Scale and center the image
    if (scale < 1) {
      $img.css({
        height:     (scale * dimensions.height)                         + "px",
        marginLeft: ((dimensions.width - scale * dimensions.width) / 2) + "px"
      });

    // Remove styling to let the browser do it's thing
    } else {
      $img.attr('style', stashedCSS[photo.id]);
      delete stashedCSS[photo.id];
    }
  }

};

// Touch code
if (hasTouchCapabilities) {

// Tap gesture recognizer
var NUMBER_OF_FINGERS_REQUIRED = 1,
    WIGGLE_ROOM  = 10, // px
    MAX_DURATION = 500; // ms

CANADA.Lightbox.prototype.tap = function () {
  this.close();
  this.element.removeEventListener('touchstart', this, false);
  this.element.removeEventListener('touchmove', this, false);
  this.element.removeEventListener('touchend', this, false);
};

CANADA.Lightbox.prototype.handleEvent = function (event) {
  switch (event.type) {
    case 'touchstart': this.touchStart(event); break;
    case 'touchmove':  this.touchMove(event); break;
    case 'touchend':   this.touchEnd(event); break;
  }
};

CANADA.Lightbox.prototype.touchStart = function (event) {
  if (event.touches.length == NUMBER_OF_FINGERS_REQUIRED) {
    this._initialTime = new Date().getTime();
    this._initialLocation = this._currentLocation = {
      x: event.pageX,
      y: event.pageY
    };
    this.element.addEventListener('touchend', this, false);
    this.element.addEventListener('touchmove', this, false);
  }
};

CANADA.Lightbox.prototype.touchMove = function (event) {
  if (event.touches.length == NUMBER_OF_FINGERS_REQUIRED) {
    this._currentLocation = {
      x: event.touches[0].pageX,
      y: event.touches[0].pageY
    };
  } else {
    this.element.removeEventListener('touchend', this, false);
    this.element.removeEventListener('touchmove', this, false);
    delete this._initialLocation;
    delete this._initialTime;
    delete this._currentLocation;
  }
};

CANADA.Lightbox.prototype.touchEnd = function (event) {
  var touchDuration = new Date().getTime() - this._initialTime;
  if (touchDuration <= MAX_DURATION) {
    var x  = this._initialLocation.x,
        y  = this._initialLocation.y,
        x0 = this._currentLocation.x,
        y0 = this._currentLocation.y;

    var distance = Math.sqrt((x -= x0) * x + (y -= y0) * y);

    if (Math.abs(distance) < WIGGLE_ROOM) {
      this.tap();
    }
  }
};

var shown = CANADA.Lightbox.prototype.shown;

CANADA.Lightbox.prototype.shown = function () {
  this.element.addEventListener('touchstart', this, false);
  shown.call(this);
};

}

}());
