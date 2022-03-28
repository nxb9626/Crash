from flask import Flask, request, make_response
app = Flask(__name__)
import chess
import random

@app.route("/")
async def ai():
    x = request.get_json()
    c_board = chess.Board(x['fen'])
    # print(c_board)
    print(c_board)
    move_list = list(c_board.legal_moves)
    # print_move_list(move_list=move_list, board=c_board)

    x = len(move_list)
    x = random.randint(0, len(move_list)-1)
    choice = move_list[x]

    return {'move':choice.uci()}


if __name__=="__main__":
    app.run(threaded=True)