"""
Rusn a bot as a server, which receives fenstrings and returns a chosen move
"""
import math
import random
import operator
import chess
import requests

from flask import Flask, request
app = Flask(__name__)

################################################################################
WHITE_BOT_URL = 'http://127.0.0.1:5000'
BLACK_BOT_URL = 'http://127.0.0.1:5000'
################################################################################

class WeightedMove:
    """
    class representing a board and move so that it can be sorted
    """
    def __init__(self,fen,move,parent=None):
        self.fen = fen
        self.move = move
        self.weight = 0
        self.parent=parent


    def __repr__(self) -> str:
        return self.fen+'\n'+self.move.uci()+'\n'+str(self.weight)

@app.route("/")
async def bot():
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    x = request.get_json()
    fen_string = x['fen']
    # print(c_board)
    # print()
    # print(chess.Board(fen_string))
    resp = requests.get('http://127.0.0.1:5001', json={'fen':fen_string})
    weights = resp.json()
    move = mini_maxi(fen=fen_string, weights=weights)
    # iterate up the tree  (max of n depth) to go with best move
    while move.parent.parent is not None:
        move = move.parent
    # move_list = list(c_board.legal_moves)
    # print_move_list(move_list=move_list, board=c_board)

    # x = len(move_list)
    # x = random.randint(0, len(move_list)-1)
    choice = move.move
    print(move)
    return {'move':choice.uci()}

def mini_maxi(fen,weights):
    """
    wrapper function for the min_max algorithm, easier to call from api call
    """
    next_boards = generate_positions(WeightedMove(fen,None,None))
    return max([ min_max(x,weights=weights) for x in next_boards],
        key=operator.attrgetter('weight'))

def min_max(weighted_move, weights, depth=0)-> WeightedMove:
    """
    fen = fenstring of current board position
    weights = weights being used to judge board
    depth = current depth in search, starts at 0
    """
    # Final depth case
    if depth==weights['max_depth']:
        return util_funciton(weighted_move, weights=weights)

    next_boards = generate_positions(weighted_move)

    # Base Case
    if not next_boards:
        if depth % 2 == 0:
            weighted_move.weight = -100
        else:
            weighted_move.weight = 100
        return weighted_move

    # Apply weights to moves
    choices = [min_max(x, weights=weights, depth=depth+1) for x in next_boards]
    # Recurse
    if depth % 2 == 0:
        best = max(choices, key=operator.attrgetter('weight')).weight
        return random.choice(list(filter(lambda x: x.weight == best, choices)))
    if depth % 2 == 1:
        worst = min(choices, key=operator.attrgetter('weight')).weight
        return random.choice(list(filter(lambda x: x.weight == worst, choices)))

def generate_positions(parent_move:WeightedMove) -> WeightedMove:
    """
    fen = fenstring of board position from which the new moves will move

    Generates new moves, which by default are unweighted
    """

    current_board = chess.Board(fen=parent_move.fen)
    # print(current_board)
    if current_board.is_game_over():
        return []
    next_boards = []
    for move in list(current_board.legal_moves):
        current_board.push(move)
        next_boards.append(WeightedMove(fen=str(current_board.board_fen()),\
            move=move,parent=parent_move))
        current_board.pop()

    return next_boards

def util_funciton(weighted_move:WeightedMove, weights:dict):
    """
    fen = fenstring of current board
    weights = weights being used to judge board

    judges the fen string based on the weights
    """
    board = chess.Board(weighted_move.fen)
    # fen = weighted_move.fen
    # board_string = fen.split(' ')[0]
    # print(board.turn)
    print(board.turn)
    #measure current players piece score
    k = len(list(board.pieces(chess.KING,board.turn))) * weights['king_weight'] * 20
    q = len(list(board.pieces(chess.QUEEN,board.turn))) * weights['queen_weight'] * 9
    r = len(list(board.pieces(chess.ROOK,board.turn))) * weights['rook_weight'] * 5
    n = len(list(board.pieces(chess.KNIGHT,board.turn))) * weights['knight_weight'] * 3
    b = len(list(board.pieces(chess.BISHOP,board.turn))) * weights['bishop_weight'] * 3
    p = len(list(board.pieces(chess.PAWN,board.turn))) * weights['pawn_weight'] 
    current_player_piece_value = p+r+n+q+b+k

    K = len(list(board.pieces(chess.KING,not board.turn))) * weights['king_weight'] * 20
    Q = len(list(board.pieces(chess.QUEEN,not board.turn))) * weights['queen_weight'] * 9
    R = len(list(board.pieces(chess.ROOK,not board.turn))) * weights['rook_weight'] * 5
    N = len(list(board.pieces(chess.KNIGHT,not board.turn))) * weights['knight_weight'] * 3
    B = len(list(board.pieces(chess.BISHOP,not board.turn))) * weights['bishop_weight'] * 3
    P = len(list(board.pieces(chess.PAWN,not board.turn))) * weights['pawn_weight']
    opponent_player_piece_value = P+R+N+Q+B+K
    print(list(board.move_stack))
    if board.is_checkmate(): 
        checkmate = math.inf
    else: 
        checkmate = 0
    # print(board.turn, current_player_piece_value- opponent_player_piece_value)
    # weights['king_weight']
    # weighted_move.weight = random.randint(0,100)
    
    weighted_move.weight = (current_player_piece_value - opponent_player_piece_value) + checkmate
    print(weighted_move)
    return weighted_move

if __name__=="__main__":
    app.run(threaded=True, port=5000)
    NEW_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen = "r1b2Bk1/pp1p4/2p4p/8/8/3P4/PPP1PPPP/RN1QKB1R w KQkq - 0 1"
    game = chess.Board(fen)
    move = WeightedMove(game.fen(),chess.Move.from_uci("e2e4"),None)
    print()
    print(util_funciton(move, weights={
        "max_depth":1,
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
    ))
    # move = mini_maxi(game.board_fen(),{'max_depth':3})
    # print()
    # print(move)
    # while move.parent.parent is not None:
    #     move = move.parent
    # game.push(move.move)
    # print(game)
    # print(game.legal_moves)

    # move = mini_maxi(game.board_fen(),{'max_depth':2})
    # print()
    # print(move)
    # game.push(move.move)
    # print(game.is_attacked_by)
    # print(game.legal_moves)
