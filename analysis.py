from pprint import pp
import chess
from weighted import WeightedMove
from adapt_server import adapt
import math

def util_funciton(current_move:WeightedMove, weights:dict)->WeightedMove:
    """
    fen = fenstring of current board
    weights = weights being used to jude board

    judges the fen string based on the weights
    """
    board = chess.Board(current_move.fen)

    pieces = get_piece_counts(board)
    scores = apply_piece_weights(pieces)

    scores.update({
        'check':get_game_is_check(board),
        'checkmate':get_game_is_checkmate(board),
        'king_moves':get_king_spaces(board),
        'central_control':get_central_squares_control(board),
        'legal_moves': get_legal_moves(board)
    })
    if weights['smart']:
        scores = adapt(scores, weights)

    board_score = sum(scores.values())

    current_move.weight = board_score
    return current_move

def get_legal_moves(board:chess.Board):
    return len(list(board.legal_moves))

def get_max_depth(board:chess.Board):
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

    #Calculating how deep should be searched
    board_piece_count = p+r+n+q+b+k+P+R+N+Q+B+K
    max_depth = math.ceil((16/(board_piece_count)+1))
    if max_depth % 2 == 0:
        max_depth-=1
    return max_depth

def get_game_is_checkmate(board:chess.Board):
    if board.is_checkmate():
            return 100000000
    return 0

def get_game_is_check(board:chess.Board):
    if board.is_check():
        return 100
    return 0

def get_piece_counts(board:chess.Board):
    pieces = {}
    #current pieces
    pieces['k'] = len(list(board.pieces(chess.KING, board.turn))) 
    pieces['q'] = len(list(board.pieces(chess.QUEEN, board.turn))) 
    pieces['r'] = len(list(board.pieces(chess.ROOK, board.turn))) 
    pieces['n'] = len(list(board.pieces(chess.KNIGHT, board.turn))) 
    pieces['b'] = len(list(board.pieces(chess.BISHOP, board.turn))) 
    pieces['p'] = len(list(board.pieces(chess.PAWN, board.turn))) 
    #opponent pieces
    pieces['K'] = len(list(board.pieces(chess.KING, not board.turn))) 
    pieces['Q'] = len(list(board.pieces(chess.QUEEN, not board.turn))) 
    pieces['R'] = len(list(board.pieces(chess.ROOK, not board.turn))) 
    pieces['N'] = len(list(board.pieces(chess.KNIGHT, not board.turn))) 
    pieces['B'] = len(list(board.pieces(chess.BISHOP, not board.turn))) 
    pieces['P'] = len(list(board.pieces(chess.PAWN, not board.turn))) 
    return pieces

def apply_piece_weights(pieces:dict):
    scores = {}
    #current pieces
    scores['k'] = pieces['k']* 20
    scores['q'] = pieces['q']* 9
    scores['r'] = pieces['r']* 5
    scores['n'] = pieces['n']* 3
    scores['b'] = pieces['b']* 3
    scores['p'] = pieces['p']* 1
    #opponent pieces
    scores['K'] = pieces['K']* -20
    scores['Q'] = pieces['Q']* -9
    scores['R'] = pieces['R']* -5
    scores['N'] = pieces['N']* -3
    scores['B'] = pieces['B']* -3
    scores['P'] = pieces['P']* -1
    return scores

def get_king_spaces(board:chess.Board):
    count = 0
    for sq in list(board.legal_moves):
        if board.piece_at(sq.from_square).symbol()=='K' or board.piece_at(sq.from_square).symbol()=='k':
            count +=1
    return count

def get_central_squares_control(board:chess.Board):
    symbols = {'P','K','Q','R','N','B'}
    if board.turn != chess.WHITE:
        symbols = {'p','k','q','r','n','b'}
    control_count = 0
    C3 = board.piece_at(chess.C3)
    if C3 is not None and C3.symbol() in symbols:
        control_count += 1
    C4 = board.piece_at(chess.C4)
    if C4 is not None and C4.symbol() in symbols:
        control_count += 1
    C5 = board.piece_at(chess.C5)
    if C5 is not None and C5.symbol() in symbols:
        control_count += 1
    C6 = board.piece_at(chess.C6)
    if C6 is not None and C6.symbol() in symbols:
        control_count += 1
    D3 = board.piece_at(chess.D3)
    if D3 is not None and D3.symbol() in symbols:
        control_count += 1
    D4 = board.piece_at(chess.D4)
    if D4 is not None and D4.symbol() in symbols:
        control_count += 1
    D5 = board.piece_at(chess.D5)
    if D5 is not None and D5.symbol() in symbols:
        control_count += 1
    D6 = board.piece_at(chess.D6)
    if D6 is not None and D6.symbol() in symbols:
        control_count += 1
    E3 = board.piece_at(chess.E3)
    if E3 is not None and E3.symbol() in symbols:
        control_count += 1
    E4 = board.piece_at(chess.E4)
    if E4 is not None and E4.symbol() in symbols:
        control_count += 1
    E5 = board.piece_at(chess.E5)
    if E5 is not None and E5.symbol() in symbols:
        control_count += 1
    E6 = board.piece_at(chess.E6)
    if E6 is not None and E6.symbol() in symbols:
        control_count += 1
    F3 = board.piece_at(chess.F3)
    if F3 is not None and F3.symbol() in symbols:
        control_count += 1
    F4 = board.piece_at(chess.F4)
    if F4 is not None and F4.symbol() in symbols:
        control_count += 1
    F5 = board.piece_at(chess.F5)
    if F5 is not None and F5.symbol() in symbols:
        control_count += 1
    F6 = board.piece_at(chess.F6)
    if F6 is not None and F6.symbol() in symbols:
        control_count += 1
    return control_count


if __name__=="__main__":
    fen_k="8/1K6/8/1k6/8/8/p7/8 b - - 0 1"
    fen_checkmate="8/Kqk5/8/8/8/8/8/8 b - - 8 9"
    fen_stalemate="2q5/K7/2k5/8/8/8/8/8 w - - 4 7"
    fen_stupid="8/8/8/8/33/8/8/8 w - - 0 1"
    board = chess.Board(fen=fen_stupid)
    weights= {
        "max_depth":3,
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
        "checking_opponent":1,
        "attacking_opponent":1
    }
    x = get_piece_counts(board) 
    pp(sum(x.values()))
    pp(sum(apply_piece_weights(x).values()))
    pp(get_king_spaces(board))
    pp(get_game_is_check(board))
    pp(get_central_squares_control(board))
    print(board)
    