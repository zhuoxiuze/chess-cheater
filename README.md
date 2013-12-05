# CHESS CHEATER
Do you suck at chess? Do you find yourself on chess.com/livechess losing all the time? **CHESS CHEATER** can help! **CHESS CHEATER** will analyze the chess board and play grandmaster-level chess for you!

## Video Demo
[Check it out on YouTube.](http://www.youtube.com/watch?v=p0AX-XSCLIk)

## Awards and Accolades
Winner of the "Most Awesome But Useless" category at Cal's 2013 HackJam!

## How it works
I built this in a few hours at HackJam 2013. It's quite hacked together.

There are 3 parts to **CHESS CHEATER**: the Chrome extension, the server application, and the chess engine.

The Chrome extension displays a control panel in the bottom right of the screen. When activated, it parses the chess board and notation to determine the move that just happened. Then it calls the API endpoint `/addmove`, and the server takes it from there...

The server, written in Python and Flask, receives a notification to move. It springs into action, spawning a subprocess which launches a grandmaster-level chess engine to determine the best move. Then the server performs the best move automatically, by moving the mouse on the screen and dropping the piece in the right location on the board.

The engine is the fabulous open source [Stockfish chess engine](http://stockfishchess.org/).

## System Requirements
**CHESS CHEATER** works with Windows or OS X. Other things you'll need: Python, Flask, and Google Chrome.

## Set it up
On OS X? Clone this repo, run the server using `python app.py`, install the Chrome extension under `chrome://extensions`, and you should be good to go.

On Windows? Follow the same steps, but you'll also need to supply an .exe file for the engine, change that string in engine.py, and uncomment the clicking function in app.py.

## License
GPLv3.