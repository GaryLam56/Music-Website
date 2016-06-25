/* Function to favorite albums */
var AlbumsListPage = {
	init: function() {
		this.$container = $('.albums-container'); /* albums-container is a class */
		this.render();							  /* this what ever tag is clicked */
		this.bindEvents();
	},

	render: function() { 

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) { /* When click on something that has class btn-favorite and is in this.$container run the following function */
			e.preventDefault(); /* prevents the default event from happening */

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) { /* Quick way to do some AJAX function*/ /*For reference: https://stackoverflow.com/questions/3835622/difference-between-json-and-ajax-when-should-what-be-used */
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active'); /* Make the star shine */
				}
			});

			return false;
		});
	}
};

/* Function to favorite songs */
var SongsListPage = {
	init: function() {
		this.$container = $('.songs-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active'); /* make the star shine */
				}
			});

			return false;
		});
	}
};

$(document).ready(function() { /* Walk for whole page to load to run javascript. Second way to do it is $(function() { });*/
	AlbumsListPage.init();
	SongsListPage.init();
});