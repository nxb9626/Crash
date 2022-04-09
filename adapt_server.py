"""
Runs an adaptation server, which receives data from the bot and determines if 
changes should be made for its decision making
"""
import pickle
import chess

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
    global moves
    moves.append(move)
    # print(moves)
    # print(fen_string)
    return {
        "max_depth":2,
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

