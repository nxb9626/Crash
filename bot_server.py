"""
Rusn a bot as a server, which receives fenstrings and returns a chosen move
"""
import math
import operator
from pprint import pp
import chess
import multiprocessing
from functools import partial
from adapt_server import adapt
import random
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
    def __init__(self,fen,move,parent=None,weight=0):
        self.fen = fen
        self.move = move
        self.weight = weight
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
    # print(fen_string)
    weights = adapt(x)# resp.json()
    move = mini_maxi(fen=fen_string, weights=weights)
    # iterate up the tree  (max of n depth) to go with best move
    while move.parent.parent is not None:
        move = move.parent

    choice = move.move
    # print(move)
    return {'move':choice.uci()}

def mini_maxi(fen, weights):
    """
    wrapper function for the min_max algorithm, easier to call from api call
    """
    
    seen_boards = set()
    seen_boards.add(fen)
    next_boards = generate_positions(WeightedMove(fen,None,None),seen_boards=seen_boards)
    pool = multiprocessing.Pool(processes=12)
    judged = pool.map(partial(min_max, weights=weights, seen_boards=seen_boards), next_boards)

    # print(judged)
    max_weight = max(judged,key=operator.attrgetter('weight')).weight 
    best_choices = [x for x in judged if x.weight == max_weight]
    # print("JUDGED: ",judged)
    print("WEIGHT:", max_weight)
    # print("CHOSEN: ",best_choices)
    return(random.choice(best_choices))
    # return max([ min_max(x,weights=weights,seen_boards=seen_boards) for x in next_boards],
        # key=operator.attrgetter('weight'))

def min_max(current_move=None, weights={}, seen_boards:set=set(), depth=0,
    alpha=WeightedMove("",move=None,parent=None,weight=-math.inf),
        beta=WeightedMove("",move=None,parent=None,weight=math.inf)
            ) -> WeightedMove:
    """
    fen = fenstring of current board position
    weights = weights being used to judge board
    depth = current depth in search, starts at 0
    """
    current_board = chess.Board(fen=current_move.fen)
    # Final depth case
    if depth==weights['max_depth']:
        return util_funciton(current_move, depth, weights=weights)
    next_boards = []
    potential_next_moves = list(current_board.legal_moves)
    #max player
    if depth % 2 == 0:
        best = WeightedMove("",move=None)
        best.weight = -math.inf
        for m in potential_next_moves:
            current_board.push(m)
            fen = current_board.fen()
            current_board.pop()
            if fen in seen_boards:
                continue

            else:
                seen_boards.add(fen)

                wm = WeightedMove(fen=str(fen),move=m,parent=current_move)
                min_max(current_move=wm,weights=weights,depth=depth+1,alpha=alpha,beta=beta)
                best = max([best,wm], key=operator.attrgetter('weight'))                
                alpha = max([alpha,best], key=operator.attrgetter('weight'))
                next_boards.append(wm)
                
                if beta.weight <= alpha.weight:
                    break
        if len(next_boards) == 0:
            return util_funciton(current_move, depth, weights=weights)
        
        return best

    #min player
    else:
        best = WeightedMove("",move=None)
        best.weight = math.inf

        for m in potential_next_moves:
            current_board.push(m)
            fen = current_board.fen()
            current_board.pop()
            
            if fen in seen_boards: 
                continue
            else:
                seen_boards.add(fen)
                wm = WeightedMove(fen=str(fen),move=m,parent=current_move)
                # Recurse to get weights correctly set
                min_max(current_move=wm,weights=weights,depth=depth+1,alpha=alpha,beta=beta)
                best = min([best,wm], key=operator.attrgetter('weight'))                
                beta = min([alpha,best], key=operator.attrgetter('weight'))
                next_boards.append(wm)
                if beta.weight <= alpha.weight:
                    break

        if len(next_boards) == 0:
            return util_funciton(current_move, depth, weights=weights)
   
        return best

def generate_positions(current_move: WeightedMove, seen_boards:set)->WeightedMove:
    """
    fen = fenstring of board position from which the new moves will move

    Generates new moves, which by default are unweighted
    """

    current_board = chess.Board(fen=current_move.fen)
    # print(current_board)
    if current_board.is_game_over():
        return []
    next_boards = []
    for move in list(current_board.legal_moves):
        current_board.push(move)
        fen = current_board.fen()
        current_board.pop()

        if fen in seen_boards:    
            continue
        else:
            seen_boards.add(fen)
            next_boards.append(WeightedMove(fen=str(fen),\
                move=move,parent=current_move))
    return next_boards

def util_funciton(current_move:WeightedMove,depth, weights:dict)->WeightedMove:
    """
    fen = fenstring of current board
    weights = weights being used to judge board

    judges the fen string based on the weights
    """
    board = chess.Board(current_move.fen)

    
    # Base Case
    # if not list(board.legal_moves):
    #     if depth % 2 == 0:
    #         current_move.weight = 1000
    #     else:
    #         current_move.weight = -1000
    #     return current_move

    # fen = current_move.fen
    # board_string = fen.split(' ')[0]
    # print(board.turn)
    # print(current_move.fen)
    # print(board.fen())
    #measure current players piece score
    k = len(list(board.pieces(chess.KING,board.turn))) * weights['king_weight'] * 20
    q = len(list(board.pieces(chess.QUEEN,board.turn))) * weights['queen_weight'] * 9
    r = len(list(board.pieces(chess.ROOK,board.turn))) * weights['rook_weight'] * 5
    n = len(list(board.pieces(chess.KNIGHT,board.turn))) * weights['knight_weight'] * 3
    b = len(list(board.pieces(chess.BISHOP,board.turn))) * weights['bishop_weight'] * 3
    p = len(list(board.pieces(chess.PAWN,board.turn))) * weights['pawn_weight'] 
    current_player_piece_value = p+r+n+q+b+k
    
    K = len(list(board.pieces(chess.KING, not board.turn))) * weights['king_weight'] * 20
    Q = len(list(board.pieces(chess.QUEEN, not board.turn))) * weights['queen_weight'] * 9
    R = len(list(board.pieces(chess.ROOK, not board.turn))) * weights['rook_weight'] * 5
    N = len(list(board.pieces(chess.KNIGHT, not board.turn))) * weights['knight_weight'] * 3
    B = len(list(board.pieces(chess.BISHOP, not board.turn))) * weights['bishop_weight'] * 3
    P = len(list(board.pieces(chess.PAWN, not board.turn))) * weights['pawn_weight']
    opponent_player_piece_value = P+R+N+Q+B+K

    if board.is_checkmate():
        checkmate = 1000
    else: 
        checkmate = 0
    # print(board.turn, current_player_piece_value- opponent_player_piece_value)
    # weights['king_weight']
    # current_move.weight = random.randint(0,100)
    
    current_move.weight = (current_player_piece_value - opponent_player_piece_value) + checkmate
    # print(current_move)
    return current_move

if __name__=="__main__":
    app.run(threaded=True, port=5000)
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_3="8/1Kn1p3/1p5N/4p1q1/4k1N1/3R2p1/Qn2B3/7R w - - 0 1"
    fen_1="8/2K1p3/1p5N/4p1q1/4k1N1/3n2p1/Q3B3/7R w - - 0 2"
    # fen = "r1b2Bk1/pp1p4/2p4p/8/8/3P4/PPP1PPPP/RN1QKB1R w KQkq - 0 1"
    game = chess.Board(fen)
    # print(len(list(game.legal_moves)))
    # print(len(list(game.pieces())))
    # move = WeightedMove(game.fen(),chess.Move.from_uci("e2e4"),None)
    # print()
    weights={
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
    # ))
    move = mini_maxi(game.board_fen(),weights)
    game.push(move.move)
    # print(move)

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
