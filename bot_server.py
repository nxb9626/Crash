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
from analysis import util_funciton 
from flask import Flask, request
from weighted import WeightedMove
app = Flask(__name__)

################################################################################
WHITE_BOT_URL = 'http://127.0.0.1:5000'
BLACK_BOT_URL = 'http://127.0.0.1:5000'
################################################################################

@app.route("/")
def bot(request):
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    x = request#.get_json()
    fen_string = x['fen']
    weights={
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
    if x['smart']:
        weights = adapt(x)
    move = mini_maxi(fen=fen_string, weights=weights)
    # iterate up the tree  (max of n depth) to go with best move
    print(move)
    choice = move.move
    # print(move)
    return {'move':choice.uci()}

def mini_maxi(fen, weights):
    """
    wrapper function for the min_max algorithm, easier to call
    """
    seen_boards = set()
    seen_boards.add(fen)
    next_boards = generate_positions(WeightedMove(fen,None,None),
        seen_boards=seen_boards)

    pool = multiprocessing.Pool(processes=15)
    judged = pool.map(partial(min_max, weights=weights, seen_boards=seen_boards), next_boards)
    pp(judged)
    best_choices = [x for x in judged if x.weight != math.inf]
    best_choices = [x for x in best_choices if x.weight != -math.inf]

    max_weight = max(best_choices,key=operator.attrgetter('weight')).weight 
    best_choices = [x for x in judged if x.weight == max_weight]

    # pp(best_choices)
    # pp(max_weight)
    choice = random.choice(best_choices)
    while choice.parent.parent is not None:
        choice = choice.parent
    # print(choice)
    return(choice)

def min_max(current_move=None, weights={}, seen_boards:set=set(), depth=0,
    alpha=WeightedMove("",move=None,parent=None,weight=-1*math.inf),
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
    print("current_turn:",current_board.turn)
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


if __name__=="__main__":
    # app.run(threaded=True, port=5000)
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_3="8/1Kn1p3/1p5N/4p1q1/4k1N1/3R2p1/Qn2B3/7R w - - 0 1"
    fen_1="8/2K1p3/1p5N/4p1q1/4k1N1/3n2p1/Q3B3/7R w - - 0 2"
    # fen = "r1b2Bk1/pp1p4/2p4p/8/8/3P4/PPP1PPPP/RN1QKB1R w KQkq - 0 1"
    fen_k = "8/1K6/8/1k6/8/8/p7/8 w - - 0 1"
    game = chess.Board(fen_1)
    # print(len(list(game.legal_moves)))
    # print(len(list(game.pieces())))
    # move = WeightedMove(game.fen(),chess.Move.from_uci("e2e4"),None)
    # print()
    # weights={
    #     "max_depth":5,
    #     "king_weight":1,
    #     "queen_weight":1,
    #     "rook_weight":1,
    #     "bishop_weight":1,
    #     "knight_weight":1,
    #     "pawn_weight":1,
    #     "pawn_structure_weight":1,
    #     "space_weight":1,
    #     "center_control":1,
    #     "opponent_threats":1,
    #     "piece_positions":{
    #         "rook_depth - 7th best":1,
    #         "bishops_on_diagonals":1,
    #         "rook_in_open_columns":1
    #     },
    #     "checking_opponent":1,
    #     "attacking_opponent":1
    # }
    # ))
    # move = mini_maxi(game.board_fen(),weights)
    # game.push(move.move)
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
