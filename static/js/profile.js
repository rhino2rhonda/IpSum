$(document).ready(function() {
	$('#nav_bar a').on('click', function() {
	    $(this).parent().parent().find('.active').removeClass('active');
	    $(this).parent().addClass('active');
	});
	$("#ad_carousel").carousel({
	 interval : 3000
	});


    $("#shop_find_pgn").on('click', function() {
    $(this).pagination({
        items: 10,
        itemsOnPage: 2,
    });
	});
	$('#shop_tab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	})
	$('#page-top').scrollspy({ target: '.navbar-fixed-top' })
	$('.dropdown-toggle').dropdown({
		
	})
});