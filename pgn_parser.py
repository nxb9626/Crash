import analysis
import chess.pgn
import chess
import pickle
import signal


# with open("measurements.obj",'rb') as measurements_file:
    # measurements = pickle.load("measurements.obj",0)
    # print(measurements)
measurements = []
def measure_positions(board:chess.Board):
    data = [analysis.get_piece_counts(board),
        len(list(board.legal_moves)),
        len(board.move_stack)
        ]
    # print('\t',data)
    return data
def measure_game(game:chess.pgn.Game):
    board = game.board()
    results = []

    for move in x.mainline_moves():
        board.push(move)
        results.append(measure_positions(board))
    return results

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        with open("measurements.obj",'wb') as measurements_file:
            pickle.dump(measurements,measurements_file,-1)
            print(measurements)
        exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    file_name = open("lichess_db_standard_rated_2013-02.pgn")
    # x = read_file_to_list_of_dicts(file_name=file_name)
    # pprint(x)       
    i=0
    while True:
        x = chess.pgn.read_game(file_name)
        if x is None:  #reached end of file
            break
        measurements.append(measure_game(x))
        i+=1
        # if i == 10000:
        #     break
        print(i,"games analyzed")
    with open("measurements.obj",'wb') as measurements_file:
            pickle.dump(measurements,measurements_file,-1)

