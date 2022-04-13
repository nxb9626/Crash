"""
Runs an adaptation server, which receives data from the bot and determines if 
changes should be made for its decision making
"""
import pickle
import chess
import math
# from flask import Flask, request
# app = Flask(__name__)

# @app.route("/")
moves = []
def adapt(request):
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    x = request#.get_json()
    fen_string = x['fen']
    move = x['move']
    moves.append(move)
    board = chess.Board(fen_string)
    k = len(list(board.pieces(chess.KING,board.turn))) 
    q = len(list(board.pieces(chess.QUEEN,board.turn)))
    r = len(list(board.pieces(chess.ROOK,board.turn))) 
    n = len(list(board.pieces(chess.KNIGHT,board.turn)))
    b = len(list(board.pieces(chess.BISHOP,board.turn)))
    p = len(list(board.pieces(chess.PAWN,board.turn)))

    K = len(list(board.pieces(chess.KING, not board.turn))) 
    Q = len(list(board.pieces(chess.QUEEN, not board.turn)))
    R = len(list(board.pieces(chess.ROOK, not board.turn))) 
    N = len(list(board.pieces(chess.KNIGHT, not board.turn)))
    B = len(list(board.pieces(chess.BISHOP, not board.turn)))
    P = len(list(board.pieces(chess.PAWN, not board.turn)))
    board_piece_count = p+r+n+q+b+k+P+R+N+Q+B+K
    # print(board_piece_count)
    # max_depth = math.ceil(6*(44-board_piece_count)/32)
    max_depth = math.ceil((16/(board_piece_count)+1))
    print("MAX_DEPTH",max_depth)
    #adapt to detpth
    # print(moves)
    # print(fen_string)
    return {
        "max_depth":5,#max_depth,
        "king_weight":1,
        "queen_weight":1,
        "rook_weight":1,
        "bishop_weight":1,
        "knight_weight":1,
        "pawn_weight":1,
        "pawn_structure_weight":1,
        "space_weight":1,
        "center_control":1,
        "opponent_threats":1,
        "piece_positions":{
            "rook_depth - 7th best":1,
            "bishops_on_diagonals":1,
            "rook_in_open_columns":1
        },
        "attacking_squares":1,
        "checking_opponent":1,
        "attacking_opponent":1
    }

# if __name__=="__main__":
    # app.run(port=5001)

