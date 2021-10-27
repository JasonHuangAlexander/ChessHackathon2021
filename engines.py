import random
import chess
import chess.engine
from time import sleep

# Josip
#stockfish_path = r"C:\Users\josiptoric\Desktop\stockfish_14_x64_avx2.exe"
#leela_path = r"C:\Users\josiptoric\Desktop\lc0-v0.28.0-windows-cpu-dnnl\lc0.exe"
#andoma_path = r"C:\Users\josiptoric\Desktop\andoma-main\main.py"

# Robert
#stockfish_path = r"C:\microsoft\hackathons\2021\hackweek\stockfish_14_win_x64\stockfish_14_win_x64\stockfish_14_x64.exe"
#leela_path = r"C:\microsoft\hackathons\2021\hackweek\lc0-v0.28.0-windows-cpu-dnnl\lc0.exe"
#andoma_path = r"C:\microsoft\repos\andoma\main.py"

# Azure
# stockfish_path = r"/home/stockfish/stockfish_14_linux_x64/stockfish_14_x64"
#leela_path = r"NOT WORKING YET"
#andoma_path = r"/home/andoma/andoma-main/main.py"

#Jason
stockfish_path = r"C:\Users\ihave\Pictures\Entity Club\code\HTML\AI stuff\stockfish_14_win_x64_avx2\stockfish_14_win_x64_avx2\stockfish_14_x64_avx2.exe"
leela_path = r"C:\microsoft\hackathons\2021\hackweek\lc0-v0.28.0-windows-cpu-dnnl\lc0.exe"
andoma_path = r"C:\microsoft\repos\andoma\main.py"

stockfish = None
leela = None
andoma = None

def get_stockfish():
    global stockfish
    if (stockfish is None):
        stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    return stockfish


def get_leela():
    global leela
    if (leela is None):
        leela = chess.engine.SimpleEngine.popen_uci(leela_path)
    return leela

def get_andoma():
    global andoma
    if (andoma is None):
        andoma = chess.engine.SimpleEngine.popen_uci(["python", andoma_path])
    return andoma

def random_move(fen: str, seconds_to_move: int) -> str:
    print("random_move - fen: " + fen)
    board = chess.Board(fen)
    moves = list(board.legal_moves)
    board.push(random.choice(moves))
    print(board)
    fen = board.fen()
    print("fen: " + fen)
    sleep(seconds_to_move)
    return fen


def uci_move(fen: str, algo: str, seconds_to_move: int) -> str:
    print("uci_move - fen: " + fen + ", algo: " + algo + ", seconds_to_move: " + str(seconds_to_move))
    board = chess.Board(fen)
    if (algo == "stockfish"):
        engine = get_stockfish()
        result = engine.play(board, chess.engine.Limit(time=seconds_to_move))
    elif (algo == "leela"):
        engine = get_leela()
        result = engine.play(board, chess.engine.Limit(time=seconds_to_move))
    elif (algo == "andoma"):
        engine = get_andoma()
        result = engine.play(board, chess.engine.Limit(time=15.0))
    board.push(result.move)
    print(board)
    fen = board.fen()
    print("fen: " + fen)
    return fen


def make_move(fen: str, algo: str, seconds_to_move: int = 2) -> str:
    if (algo == "random"):
        return random_move(fen, seconds_to_move)
    elif (algo == "stockfish" or algo == "leela" or algo == "andoma"):
        return uci_move(fen, algo, seconds_to_move)