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
moveTime = "100"

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
	return "Success"

@app.route('/addmove', methods=['GET'])
def addMove():
	the_move = request.args['move']
	if len(moves) > 0 and moves[len(moves) - 1] == the_move:
		return "Already added"
	moves.append(the_move)
	return "Success"

@app.route('/clear', methods=['GET'])
def clearMoves():
	del(moves[0:len(moves)])
	return "Success"

@app.route('/setspeed', methods=['GET'])
def setSpeed():
	global moveTime
	moveTime = request.args['time']
	return 'Time changed to ' + moveTime + ' ms'

@app.route('/makemove', methods=['GET'])
def makeMove():
	best_move, analysis = engine.get_best_move(moves, moveTime)
	# convert to coordinates
	amount_to_shift = boardSide // 8

	firstX = boardLeft + amount_to_shift / 2 + letterToNumber(best_move[0]) * amount_to_shift
	firstY = boardTop + amount_to_shift / 2 + amount_to_shift * (8 - numberAsCharToNumber(best_move[1]))

	secondX = boardLeft + amount_to_shift / 2 + letterToNumber(best_move[2]) * amount_to_shift
	secondY = boardTop + amount_to_shift / 2 + amount_to_shift * (8 - numberAsCharToNumber(best_move[3]))

	click2(int(firstX), int(firstY))
	time.sleep(0.025)
	click2(int(secondX), int(secondY))
	moves.append(best_move)

	to_return = 'Stockfish did: ' + best_move + ' Analysis: ' + analysis

	return to_return

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