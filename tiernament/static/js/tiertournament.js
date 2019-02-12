$(document).ready(function() {
	var playerNum = 0;

	$(document).on('click', '#plus-button', function() {
		$('#players').append("<div class='player-entry' id='player" + playerNum++ + "'>Name:<input type='text' name='playername" + playerNum + "'><a href='#'>X</a></div>");
	});

	$(document).on('click', '.player-entry a', function(e) {
		e.preventDefault();
		$(this).parent().remove();
	});

	function setPlacements(placements) {
		for(var i = 0; i < placements.keys;  i++){
			alert(placements);
		}
	}

	setPlacements({{ placements }});
});

