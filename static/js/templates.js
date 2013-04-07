CANADA.TEMPLATES = {};

CANADA.render = function (templateName, context) {
  return CANADA.TEMPLATES[templateName](context);
};

CANADA.TEMPLATES['gallery'] = function (context) {
  var buffer = [];

  buffer.push('<div class="swipe" id="gallery-' + context.id + '">');
  buffer.push(CANADA.TEMPLATES['photos'](context.photos));
  buffer.push('</div>');

  return buffer.join('');
};

CANADA.TEMPLATES['lightbox'] = function () {
  var buffer = [];

  buffer.push('<div class="lightbox">');
  buffer.push('<div class="prev"></div>');
  buffer.push('<div class="next"></div>');
  buffer.push('<div class="close"></div>');
  buffer.push('</div>');

  return buffer.join('');
};

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
