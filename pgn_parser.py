import analysis
import chess.pgn
import chess
def measure_positions(board):
    analysis.get_piece_counts()
def measure_game(game:chess.pgn.Game):
    board = game.board()
    for move in x.mainline_moves():
        board.push(move)
        print(board)

if __name__ == "__main__":
    file_name = open("example.pgn")
    # x = read_file_to_list_of_dicts(file_name=file_name)
    # pprint(x)
    i = 0
    while True:
        x = chess.pgn.read_game(file_name)
        #reached end of file
        if x is None:
            break
        i+=1
        print(i)
        print(x)
    