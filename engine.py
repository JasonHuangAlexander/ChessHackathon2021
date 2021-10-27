import random
import chess
import chess.engine

from flask import Flask, request, jsonify
app = Flask(__name__)

stockfish = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\josiptoric\Desktop\stockfish_14_x64_avx2.exe")
leela = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\josiptoric\Desktop\lc0-v0.28.0-windows-cpu-dnnl\lc0.exe")
andoma = chess.engine.SimpleEngine.popen_uci(
    ["python", r"C:\Users\josiptoric\Desktop\andoma-main\main.py"])


def uci_move(position, alg, time_to_move):
    if (alg == "stockfish"):
        engine = stockfish
    elif (alg == "leela"):
        engine = leela
    elif (alg == "andoma"):
        engine = andoma
    board = chess.Board()
    result = engine.play(board, chess.engine.Limit(time=time_to_move))
    board.push(result.move)
    return board.fen()


def random_move(position):
    board = chess.Board(position)
    moves = list(board.legal_moves)
    board.push(random.choice(moves))
    return board.fen()


def make_move(position, alg, time):
    if (alg == "random"):
        return random_move(position)
    elif (alg == "stockfish" or alg == "leela" or alg == "andoma"):
        return uci_move(position, alg, time)


@app.route('/make_move', methods=['POST'])
def my_test_endpoint():
    input_json = request.get_json(force=True)
    print(input_json)
    move = make_move(input_json["fen"], input_json["alg"], input_json["time"])
    return jsonify(move)


if __name__ == '__main__':
    app.run(debug=True)
