


// add padding top to show content behind navbar
$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

// detect scroll top or down
if ($('.smart_scroll').length > 0) { // check if element exists
    let last_scroll_top = 0;
    $(window).on('scroll', function() {
        let scroll_top = $(this).scrollTop();
        if(scroll_top < last_scroll_top) {
            $('.smart_scroll').removeClass('scrolled-down').addClass('scrolled-up');
        }
        else {
            $('.smart_scroll').removeClass('scrolled-up').addClass('scrolled-down');
        }
        last_scroll_top = scroll_top;
    });
}