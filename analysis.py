from pprint import pp
from tabnanny import check
import chess
from weighted import WeightedMove

def util_funciton(current_move:WeightedMove,depth, weights:dict)->WeightedMove:
    """
    fen = fenstring of current board
    weights = weights being used to jude board

    judges the fen string based on the weights
    """
    board = chess.Board(current_move.fen)

    game_status = get_game_status(board)
    
    pieces = get_piece_counts(board)
    piece_scores = apply_piece_weights(pieces,weights)
    piece_worth = sum(piece_scores.values())
    
    board_score = piece_worth + game_status

    setattr(current_move,'weight',board_score)
    return current_move

def get_game_status(board:chess.Board):
    game_status = 0
    if board.is_checkmate():
        game_status += 1000
    elif board.is_check():
        game_status += 100
    return game_status

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

def apply_piece_weights(pieces:dict,weights:dict):
    scores = {}
    #current pieces
    scores['k'] = pieces['k']* weights['king_weight'] * 20
    scores['q'] = pieces['q']* weights['queen_weight'] * 9
    scores['r'] = pieces['r']* weights['rook_weight'] * 5
    scores['n'] = pieces['n']* weights['knight_weight'] * 3
    scores['b'] = pieces['b']* weights['bishop_weight'] * 3
    scores['p'] = pieces['p']* weights['pawn_weight'] * 1
    #opponent pieces
    scores['K'] = pieces['K']* weights['king_weight'] * -20
    scores['Q'] = pieces['Q']* weights['queen_weight'] * -9
    scores['R'] = pieces['R']* weights['rook_weight'] * -5
    scores['N'] = pieces['N']* weights['knight_weight'] * -3
    scores['B'] = pieces['B']* weights['bishop_weight'] * -3
    scores['P'] = pieces['P']* weights['pawn_weight'] * -1
    return scores

def get_king_spaces(board:chess.Board):
    count = 0
    for sq in list(board.legal_moves):
        if board.piece_at(sq.from_square).symbol()=='K' or board.piece_at(sq.from_square).symbol()=='k':
            count +=1
    return count



if __name__=="__main__":
    fen_k="8/1K6/8/1k6/8/8/p7/8 b - - 0 1"
    fen_checkmate="8/Kqk5/8/8/8/8/8/8 b - - 8 9"
    fen_stalemate="2q5/K7/2k5/8/8/8/8/8 w - - 4 7"
    board = chess.Board(fen=fen_k)
    weights= {
        "max_depth":5,
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
    pp(sum(apply_piece_weights(x, weights).values()))
    pp(get_king_spaces(board))
    pp(get_game_status(board))

    print(board)
    
    