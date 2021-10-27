# INTRODUCTION

Instructions for how to download and test engines outside of the webapp.

# DEPLOY ENGINE LOCALLY
1. Download engines
   1. Stockfish: https://stockfishchess.org/download/
   2. Leela: https://lczero.org/play/download/
   3. Andoma: https://github.com/healeycodes/andoma
2. Set engine paths in engine.py
3. Set environment variables for Flask
   1. $env:FLASK_APP = "engine"
4. flask run
5. Make POST request to /make_move with following body contents:
```
{
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "alg": "stockfish",
    "time": 3
}

"fen" -> FEN status of the game
"alg" -> choose between "random", "stockfish", "leela" or "andoma"
"time" -> time in seconds for engine to think
```
6. Result is the FEN position after engine has played its move