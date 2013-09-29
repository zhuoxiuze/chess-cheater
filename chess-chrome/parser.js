var controlpanel = '<div id="CHESS_SETTINGS">\
<a href="#" id="CHESS_SETTINGS_START">Start</a><br>\
<a href="#" id="CHESS_SETTINGS_STOP">Stop</a><br>\
<a href="#" id="CHESS_SETTINGS_RESET">Reset</a>\
</div>';

$('body').append(controlpanel);
$('#CHESS_SETTINGS').css({
	position: 'absolute',
	bottom: 0,
	right: 0,
	height: '200px',
	width: '300px',
	background: '#be0c0b',
	'z-index': '100'
});
$('#CHESS_SETTINGS a').css({
	color: 'white',
	'font-family': 'Segoe UI',
	'font-size': '20px'
});

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
	//alert('prepare for awesomeness');
	//$('body').bind('DOMSubtreeModified', function() {
		// find out whether i am top or bottom
		var mySide = $(".plyrb:contains('electrocuter')").attr('id');
		var currSide = $('.timerin.active').parent().attr('id');
		//var moved = false;
		//console.log(mySide);
		//console.log(currSide);
		//if (mySide != currSide) {
		//	moved = false;
		//}
		if (true) {
			// set position ... done
			var btop = $('#chessboard_dummy').offset().top;
			var bleft = $('#chessboard_dummy').offset().left;
			var bside = $('#chessboard_dummy').width();
			$.get('http://localhost:5000/position', {boardTop: btop + 60,
				boardLeft: bleft,
				boardSide: bside});

			// add move ... todo
			// yellow squares
			var squares = $('div').filter(function() {
				return $(this).css('border') == '3px solid rgb(255, 255, 51)';
			});
			if (squares.length != 2) {
				$.get('http://localhost:5000/makemove?');
				//moved = true;
				return;
			}
			var num1 = get_number_reverse(parseInt($(squares[0]).css('top')), bside);
			var let1 = get_letter(parseInt($(squares[0]).css('left')), bside);
			var num2 = get_number_reverse(parseInt($(squares[1]).css('top')), bside);
			var let2 = get_letter(parseInt($(squares[1]).css('left')), bside);
			var sq1 = let1 + num1;
			var sq2 = let2 + num2;

			// convert top and left to notation
			// var bcell = bside / 8;


			// last notation

			var finalPos = $('.notationVertical:last-of-type .mhl a').text().replace('+','');
			if (finalPos == "O-O") {
				// todo castle
			} else if (finalPos == "O-O-O") {

			}
			finalPos=finalPos.substring(finalPos.length - 2);
			// queening todo

			var combined;
			if (sq1 == finalPos) {
				combined = sq2 + finalPos;
			} else {
				combined = sq1 + finalPos;
			}
			$.get('http://localhost:5000/addmove', {move: combined}, function() {
				alert('added move ' + combined);
				// when adding move returns
				$.get('http://localhost:5000/makemove?');
			});

			
		}

		
	//});
});

$("#CHESS_SETTINGS_STOP").click(function() {
	$('body').unbind('DOMSubtreeModified');
});

$("#CHESS_SETTINGS_RESET").click(function() {
	$.get('http://localhost:5000/clear?');
	$('#cheat-stat').html('');
});