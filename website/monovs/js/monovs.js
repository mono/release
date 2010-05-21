$(document).ready(function () {

  $.gaTracker('UA-76510-1');
  $('.feature').addClass('jquery').find('a')
    .each(function () {
      $(this).attr('href', function (href) {
        return $(this).attr('href') + '?nc=1';
      });
    })
    .each(function () {
      var link = $(this).attr('href');
      $(this).parents('.feature').wrap($('<a>', { 'href': link, 'rel': 'feat' })).parents('a').fancybox({
        'cyclic': true,
        'overlayShow': false,
        'speedIn': 200,
        'speedOut': 500,
        'changeFade': 100,
        'imageScale': true,
        'transitionIn': 'fade',
        'transitionOut': 'fade',
//        'autoDimensions': false,
        'width': '700px',
        'height': '700px'
//        'overlayColor': '#000',
//        'overlayOpacity': 0.7
      });
    });
});
