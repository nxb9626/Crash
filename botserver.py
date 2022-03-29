import random
from time import sleep
import chess
import operator
from flask import Flask, request
app = Flask(__name__)

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
    print()
    print(chess.Board(fen_string))
    move = mini_maxi(fen=fen_string, weights={'max_depth':0})
    # iterate up the tree  (max of n depth) to go with best move
    while move.parent.parent is not None:
        move = move.parent
    # move_list = list(c_board.legal_moves)
    # print_move_list(move_list=move_list, board=c_board)

    # x = len(move_list)
    # x = random.randint(0, len(move_list)-1)
    choice = move.move

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
        return 1

    # Apply weights to moves
    choices = [min_max(x, weights=weights, depth=depth+1) for x in next_boards]
    # Recurse
    if depth % 2 == 0:
        return max(choices, key=operator.attrgetter('weight'))
    if depth % 2 == 1:
        return min(choices, key=operator.attrgetter('weight'))

def generate_positions(parent_move) -> WeightedMove:
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
        next_boards.append(WeightedMove(fen=str(current_board.board_fen()),move=move,parent=parent_move))
        current_board.pop()

    return next_boards

def util_funciton(weighted_move, weights):
    """
    fen = fenstring of current board
    weights = weights being used to judge board

    judges the fen string based on the weights
    """
    weighted_move.weight = random.randint(0,100)
    return weighted_move

if __name__=="__main__":
    app.run(threaded=True, port=5000)
    # game = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
  
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
