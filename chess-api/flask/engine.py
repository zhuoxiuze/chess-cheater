import subprocess

stockfish = subprocess.Popen(["./stockfish-dd-64-modern"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def get_best_move(moves_list, move_time):
	moves_as_str = ' '.join(moves_list)
	stockfish.stdin.write(('setoption name Threads value 2\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('setoption name Hash value 128\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('setoption name OwnBook value true\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('position startpos moves ' + moves_as_str + '\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('go movetime ' + move_time + '\n').encode('utf-8'))
	stockfish.stdin.flush()
	
	bestmove = "";
	analysis = "";

	while True:
		line = stockfish.stdout.readline().decode().rstrip()
		if "score cp" in line:
			analysis = line
		if "bestmove" in line:
			bestmove = line
			break
	
	return bestmove.split()[1], analysis

