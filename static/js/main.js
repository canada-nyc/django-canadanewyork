CANADA = {
  // Photo information is provided by id
  Gallery: {},
  TEMPLATES: {}
};

// Ignore list based off: https://gist.github.com/1878283
CANADA.RAVEN_CONFIG = {
  // Will cause a deprecation warning, but the demise of `ignoreErrors` is still under discussion.
  // See: https://github.com/getsentry/raven-js/issues/73
  ignoreErrors: [
    // Random plugins/extensions
    'top.GLOBALS',
    // See: http://blog.errorception.com/2012/03/tale-of-unfindable-js-error.html
    'originalCreateNotification',
    'canvas.contentDocument',
    'MyApp_RemoveAllHighlights',
    'http://tt.epicplay.com',
    'Can\'t find variable: ZiteReader',
    'jigsaw is not defined',
    'ComboSearch is not defined',
    'http://loading.retry.widdit.com/',
    'atomicFindClose',
    // Facebook borked
    'fb_xd_fragment',
    // ISP "optimizing" proxy - `Cache-Control: no-transform` seems to reduce this. (thanks @acdha)
    // See http://stackoverflow.com/questions/4113268/how-to-stop-javascript-injection-from-vodafone-proxy
    'bmi_SafeAddOnload',
    'EBCallBackMessageReceived',
    // See http://toolbar.conduit.com/Developer/HtmlAndGadget/Methods/JSInjection.aspx
    'conduitPage',
    // Generic error code from errors outside the security sandbox
    // You can delete this if using raven.js > 1.0, which ignores these automatically.
    'Script error.'
  ],
  ignoreUrls: [
    // Facebook flakiness
    /graph\.facebook\.com/i,
    // Facebook blocked
    /connect\.facebook\.net\/en_US\/all\.js/i,
    // Woopra flakiness
    /eatdifferent\.com\.woopra-ns\.com/i,
    /static\.woopra\.com\/js\/woopra\.js/i,
    // Chrome extensions
    /extensions\//i,
    /^chrome\:\/\//i,
    // Other plugins
    /127\.0\.0\.1\:4001\/isrunning/i,  // Cacaoweb
    /webappstoolbarba\.texthelp\.com\//i,
    /metrics\.itunes\.apple\.com\.edgesuite\.net\//i
  ]
};

// Configure Raven and install default handler to capture uncaught exceptions
$(document).ready(function () {
  Raven.config(CANADA.SENTRY_DSN, CANADA.RAVEN_CONFIG).install();

  // Initialize photo galleries
  $('.gallery').on('click', function () {
    var id = $(this).attr('id'),
        photos = CANADA.Gallery[id],
        swipe;
    $('.lightbox').append('<div class="swipe" id="gallery-' + id + '"></div>');
    $('#gallery-' + id).html(CANADA.TEMPLATES['photos'](photos));
    $('.lightbox').fadeIn(function () {
      swipe = Swipe($('#gallery-' + id)[0]);
      $('.prev').on('click', function () {
        swipe.prev();
      });
      $('.next').on('click', function () {
        swipe.next();
      });
    });

    $('.close').on('click', function () {
      $('.lightbox').fadeOut(function () {
        if (swipe) swipe.kill();
        $('#gallery-' + id).remove();
      });
      return false;
    });
  });

  $('.open-gallery').on('click', function () {
    $($(this).attr('href')).click();
  });

  $('body').append('<div class="lightbox"><div class="prev"></div><div class="next"><div class="close"></div></div></div>');
});

CANADA.TEMPLATES['photos'] = function (photos) {
  var buffer = [];

  buffer.push('<div class="swipe-wrap">');
  for (var i = 0, len = photos.length; i < len; i++) {
    buffer.push(CANADA.TEMPLATES['photo'](photos[i]));
  }
  buffer.push('</div>');
  return buffer.join('');
};

CANADA.TEMPLATES['photo'] = function (photo) {
  var buffer = [],
      sizes = photo.sizes,
      image;

  image = sizes.large || sizes.thumb;
  buffer.push('<div>');
  buffer.push('<figure style="max-width: ' + image.width + 'px">');
  buffer.push('<img src="' + image.url + '" title="' + photo.title + '"/>');
  buffer.push('<aside>');
  buffer.push('<em>' + photo.title + '</em>');
  buffer.push(photo.caption);
  buffer.push('</aside>');
  buffer.push('</figure>');
  buffer.push('</div>');
  return buffer.join('');
};
