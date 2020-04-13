$('.pre-arrow').on('click', function() {
    $(this).children().toggleClass('active');
});

$('.icon-expandable').on('click', function() {
    $(this).toggleClass('is-expanded');
});

$('.icon-expandable-180').on('click', function() {
    $(this).toggleClass('is-expanded');
});