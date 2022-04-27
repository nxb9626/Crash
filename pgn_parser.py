from pandas import DataFrame
import analysis
import chess.pgn
import chess
import pickle
import numpy as np
from sklearn import linear_model, preprocessing
import matplotlib.pyplot as plt 

measurements = []
def measure_positions(board:chess.Board, is_good):
    data = analysis.get_piece_counts(board)
    data['p'] = data['p'] * is_good
    data['r'] = data['r'] * is_good
    data['k'] = data['k'] * is_good
    data['b'] = data['b'] * is_good
    data['q'] = data['q'] * is_good
    data['n'] = data['n'] * is_good
    data['P'] = data['P'] * is_good
    data['R'] = data['R'] * is_good
    data['K'] = data['K'] * is_good
    data['B'] = data['B'] * is_good
    data['Q'] = data['Q'] * is_good
    data['N'] = data['N'] * is_good
    data['king_moves'] = analysis.get_king_spaces(board)
    data['check'] = 0
    if board.is_check(): 
        data['check'] = 1 
    data['check'] = data['check'] * is_good

    data["legal_moves"]  =   len(list(board.legal_moves)) * is_good
    data["game_depth"]  = len(board.move_stack)
    data['central_control'] = analysis.get_central_squares_control(board) * is_good
    return data

def measure_game(game:chess.pgn.Game):
    board = game.board()
    results = []

    move_count = 0
    for move in x.mainline_moves():
        # print(move_count)
        board.push(move)
        move_count +=1
        if board.turn != chess.WHITE:
            continue

        is_good = -1
        if game.headers['Result'] == '1-0':
            is_good = 1

        score = measure_positions(board, is_good)
        results.append(score)

    return results

if __name__ == "__main__":
    file_name = open("lichess_db_standard_rated_2013-01.pgn")
    measurements = []
    i=0
    x = chess.pgn.read_game(file_name)

    while x is not None:
        if x.headers['Result'] != '1-0':
            x = chess.pgn.read_game(file_name)
            continue
        if x.headers['Event'] != "Rated Classical game":
            x = chess.pgn.read_game(file_name)
            continue
        if i > 100:
            break
        measurements.extend(measure_game(x))
        i+=1
        print(i,"games analyzed")
        x = chess.pgn.read_game(file_name)

    organized_chess_data = DataFrame(measurements)
    min_max_scaling = preprocessing.MinMaxScaler()
    cols = organized_chess_data.columns
    game_depth = organized_chess_data['game_depth']
    
    normalized_ocd = min_max_scaling.fit_transform(organized_chess_data.values)
    norm_ocd_df = DataFrame(normalized_ocd, columns=cols)

    print(norm_ocd_df)
    LR = linear_model.LinearRegression()
   
    y_data = norm_ocd_df['game_depth']
    x_data = norm_ocd_df.drop('game_depth',axis=1)
    
    LR.fit(x_data,y_data)

    names=LR.feature_names_in_
    b = LR.intercept_
    m = LR.coef_
    model = {}
    i=0
    with open("ocd.obj",'wb') as measurements_file:
        pickle.dump((names,m,b),measurements_file,-1)
    for name in names:
        model[name] = m[i]
    print(names)
    print("Coefficients:      ", m)
    print("Intercept:         ", b)
    np.set_printoptions(precision=5)
    x = 'game_depth'
    y = 'central_control'
    
    plt.plot(norm_ocd_df[x], norm_ocd_df[y],'o')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

    
