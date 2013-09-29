import subprocess

stockfish = subprocess.Popen(["stockfish.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def get_best_move(moves_list):
	"""
	>>> get_best_move([])
	'e2e4'
	>>> get_best_move(['e2e4'])
	'e7e5'
	>>> get_best_move(['e2e4', 'e7e5'])
	'g1f3'
	"""
	moves_as_str = ' '.join(moves_list)
	stockfish.stdin.write(('position startpos moves ' + moves_as_str + '\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write('go movetime 1000\n'.encode('utf-8'))
	stockfish.stdin.flush()
	
	while True:
		line = stockfish.stdout.readline().decode().rstrip()
		if "bestmove" in line:
			break
	
	return line.split()[1]

