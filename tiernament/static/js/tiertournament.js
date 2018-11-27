$(document).ready(function() {
	var playerNum = 0;

	$(document).on('click', '#plus-button', function() {
		$('#players').append("<div class='player-entry' id='player" + playerNum++ + "'>Name:<input type='text' name='playername'><a href='#'>X</a></div>");
	});

	$(document).on('click', '.player-entry a', function(e) {
		e.preventDefault();
		$(this).parent().remove();
	});
});

