import subprocess

stockfish = subprocess.Popen(["stockfish.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def get_best_move(moves_list):
	moves_as_str = ' '.join(moves_list)
	stockfish.stdin.write(('setoption name Threads value 2\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('setoption name Hash value 128\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('setoption name OwnBook value true\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write(('position startpos moves ' + moves_as_str + '\n').encode('utf-8'))
	stockfish.stdin.flush()
	stockfish.stdin.write('go movetime 100\n'.encode('utf-8'))
	stockfish.stdin.flush()
	
	while True:
		line = stockfish.stdout.readline().decode().rstrip()
		if "bestmove" in line:
			break
	
	return line.split()[1]

