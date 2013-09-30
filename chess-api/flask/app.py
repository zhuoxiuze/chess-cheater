#!flask/bin/python
from flask import Flask, request
import subprocess, pipes
import engine
import ctypes
import time

def click2(x, y):
	ctypes.windll.user32.SetCursorPos(x, y)
	ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)
	ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)
app = Flask(__name__)

# board positions
boardTop = 0
boardLeft = 0
boardSide = 0
moves = []
stockfish = None

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/position', methods=['GET'])
def setPosition():
	global boardTop
	global boardLeft
	global boardSide
	boardTop = int(request.args['boardTop'])
	boardLeft = int(request.args['boardLeft'])
	boardSide = int(request.args['boardSide'])
	print(boardTop, boardLeft, boardSide)
	return "Success"

@app.route('/addmove', methods=['GET'])
def addMove():
	print('adding a move')
	the_move = request.args['move']
	if len(moves) > 0 and moves[len(moves) - 1] == the_move:
		return "Already added"
	print('the move is',the_move)
	moves.append(the_move)
	print('moves looks like [',', '.join(moves),']')
	return "Success"

@app.route('/clear', methods=['GET'])
def clearMoves():
	print('clearing all moves')
	del(moves[0:len(moves)])
	print('moves now has',len(moves),'elements')
	return "Success"


@app.route('/makemove', methods=['GET'])
def makeMove():
	best_move = engine.get_best_move(moves)
	# convert to coordinates
	amount_to_shift = boardSide // 8

	firstX = boardLeft + amount_to_shift / 2 + letterToNumber(best_move[0]) * amount_to_shift
	firstY = boardTop + amount_to_shift / 2 + amount_to_shift * (8 - numberAsCharToNumber(best_move[1]))

	secondX = boardLeft + amount_to_shift / 2 + letterToNumber(best_move[2]) * amount_to_shift
	secondY = boardTop + amount_to_shift / 2 + amount_to_shift * (8 - numberAsCharToNumber(best_move[3]))

	click2(int(firstX), int(firstY))
	time.sleep(0.1)
	click2(int(secondX), int(secondY))
	moves.append(best_move)
	return best_move

def numberAsCharToNumber(char):
	"""
	>>> numberAsCharToNumber('0')
	0
	>>> numberAsCharToNumber('5')
	5
	>>> numberAsCharToNumber('9')
	9
	"""
	return ord(char) - 48

def letterToNumber(letter):
	"""
	>>> letterToNumber('a')
	0
	>>> letterToNumber('b')
	1
	>>> letterToNumber('h')
	7
	"""
	return ord(letter) - 97

if __name__ == '__main__':
    app.run(debug = True)