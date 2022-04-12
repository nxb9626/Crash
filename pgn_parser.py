import analysis
import chess.pgn
import chess


if __name__ == "__main__":
    file_name = open("example.pgn")
    # x = read_file_to_list_of_dicts(file_name=file_name)
    # pprint(x)
    x = chess.pgn.read_game(file_name)
    board = x.board()
    for move in x.mainline_moves():
        board.push(move)
        print(board)
