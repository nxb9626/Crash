import chess
from weighted import WeightedMove
def util_funciton(current_move:WeightedMove,depth, weights:dict)->WeightedMove:
    """
    fen = fenstring of current board
    weights = weights being used to judge board

    judges the fen string based on the weights
    """
    board = chess.Board(current_move.fen)    
    if board.is_checkmate():
        checkmate = 1000
    elif board.is_check():
        checkmate = 100
    else: 
        checkmate = 0

    board_score = sum({
        sum(get_current_player_piece_scores(board,weights)),
        checkmate,
        get_king_spaces(board),
        -sum(get_opponent_piece_scores(board=board,weights=weights)),
        # -depth,
        }
    ) 
    setattr(current_move,'weight',board_score/(depth+1))
    # print(current_move.weight)
    # print(current_move)
    return current_move

def get_current_player_piece_scores(board:chess.Board,weights:dict):
    # k = len(list(board.pieces(chess.KING,board.turn))) * weights['king_weight'] * 20
    q = len(list(board.pieces(chess.QUEEN,board.turn))) * weights['queen_weight'] * 9
    r = len(list(board.pieces(chess.ROOK,board.turn))) * weights['rook_weight'] * 5
    n = len(list(board.pieces(chess.KNIGHT,board.turn))) * weights['knight_weight'] * 3
    b = len(list(board.pieces(chess.BISHOP,board.turn))) * weights['bishop_weight'] * 3
    p = len(list(board.pieces(chess.PAWN,board.turn))) * weights['pawn_weight'] 
    return (p,r,n,q,b)

def get_opponent_piece_scores(board:chess.Board,weights:dict):
    # K = len(list(board.pieces(chess.KING, not board.turn))) * weights['king_weight'] * 20
    Q = len(list(board.pieces(chess.QUEEN, not board.turn))) * weights['queen_weight'] * 9
    R = len(list(board.pieces(chess.ROOK, not board.turn))) * weights['rook_weight'] * 5
    N = len(list(board.pieces(chess.KNIGHT, not board.turn))) * weights['knight_weight'] * 3
    B = len(list(board.pieces(chess.BISHOP, not board.turn))) * weights['bishop_weight'] * 3
    P = len(list(board.pieces(chess.PAWN, not board.turn))) * weights['pawn_weight']
    return (P,R,N,Q,B)

def get_king_spaces(board:chess.Board):
    count = 0
    for sq in list(board.legal_moves):
        if board.piece_at(sq.from_square).symbol()=='K':
            count +=1
    return count



if __name__=="__main__":
    fen_k="8/1K6/8/pk6/8/8/8/8 w - - 0 1"

    board = chess.Board(fen=fen_k)
    print(get_king_spaces(board))
    
    