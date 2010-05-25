$(document).ready(function () {

  $.gaTracker('UA-76510-1');
  $('.feature').addClass('jquery').find('a')
    .each(function () {
      var href = $(this).attr('href') + '?nc=1',
      heading = $(this).text();
      $(this).parent("h2").text(heading).parent('.feature')
        .wrap($('<a>', { 'href': href, 'rel': 'feat' }))
        .parent('a').fancybox({
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
