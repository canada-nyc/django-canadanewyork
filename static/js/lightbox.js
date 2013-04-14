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
  },

  show: function (galleryId) {
    var gallery = CANADA.store.find('gallery', galleryId);
    $('.lightbox').append(CANADA.render('gallery', gallery));
    this.element = $('#gallery-' + galleryId)[0];
    if (gallery.photos.length == 1) {
      $('.lightbox').find('.next, .prev').hide();
    } else {
      $('.lightbox').find('.next, .prev').show();
    }

    $('.lightbox').fadeIn(bind(this.shown, this));
  },

  shown: function () {
    this.swipe = Swipe(this.element);
    this.isShowing = true;
  }

};

}());