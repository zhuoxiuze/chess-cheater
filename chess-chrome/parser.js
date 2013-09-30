var controlpanel = '<div id="CHESS_SETTINGS">\
<h1>Chess Cheater Deluxe Pro Alpha</h1>\
<a href="#" id="CHESS_SETTINGS_START">Auto-Move</a>\
<a href="#" id="CHESS_SETTINGS_RESET">Clear Move History</a>\
<p>Status Text</p>\
</div>';

$('body').append(controlpanel);

function status(text) {
	$('#CHESS_SETTINGS p').text(text);
}

function get_letter(pos, bside) {
	var num = get_number(pos, bside) - 1;
	// from 0 to 7
	var ascii = 97 + num;
	var str = String.fromCharCode(ascii);
	return str.charAt(0);
}
function get_number(pos, bside) {
	// from 1 to 8
	return Math.floor((pos + 5) / (bside / 8)) + 1;
}
function get_number_reverse(pos, bside) {
	return 9 - get_number(pos, bside);
}

$("#CHESS_SETTINGS_START").click(function() {
	var username = $('#layout_top_username .chess_com_username_link').text();

	// Am I top or bottom?
	var mySide = $(".plyrb:contains('"+ username + "')").attr('id');
	var currSide = $('.timerin.active').parent().attr('id');

	if (mySide == currSide) {
		// Board positioning
		var btop = $('#chessboard_dummy').offset().top;
		var bleft = $('#chessboard_dummy').offset().left;
		var bside = $('#chessboard_dummy').width();
		$.get('http://localhost:5000/position', {boardTop: btop + 60,
			boardLeft: bleft,
			boardSide: bside});

		// The yellow squares
		var squares = $('div').filter(function() {
			return $(this).css('border') == '3px solid rgb(255, 255, 51)';
		});
		if (squares.length != 2) {
			$.get('http://localhost:5000/makemove?', function() {
				status('Made the first move');
			});
			return;
		}
		var num1 = get_number_reverse(parseInt($(squares[0]).css('top')), bside);
		var let1 = get_letter(parseInt($(squares[0]).css('left')), bside);
		var num2 = get_number_reverse(parseInt($(squares[1]).css('top')), bside);
		var let2 = get_letter(parseInt($(squares[1]).css('left')), bside);
		var sq1 = let1 + num1;
		var sq2 = let2 + num2;

		var finalPos = $('.notationVertical:last-of-type .mhl a').text().replace('+','');
		if (finalPos.indexOf("=") != -1) {
			finalPos = finalPos.substring(0,2) + finalPos.substring(3,4).toLowerCase();
		} else if (finalPos == "O-O" || finalPos == "O-O-O") {
			if (sq1.indexOf("e") != -1) {
				finalPos = sq2
			} else {
				finalPos = sq1
			}
		} else {
			finalPos=finalPos.substring(finalPos.length - 2);
		}

		var combined;
		if (sq1 == finalPos) {
			combined = sq2 + finalPos;
		} else {
			combined = sq1 + finalPos;
		}
		status('Enemy did ' + combined);
		$.get('http://localhost:5000/addmove', {move: combined}, function() {
			$.get('http://localhost:5000/makemove?', function(data) {
				status('Stockfish did ' + data);
			});
		});
	} else {
		status("You are " + mySide + " but it is " + currSide + "'s turn");
	}
			
});

$("#CHESS_SETTINGS_RESET").click(function() {
	$.get('http://localhost:5000/clear?', function() {
		status('Cleared');
	});
	
});