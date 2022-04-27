from itertools import count
from pprint import pp
from pandas import DataFrame
import analysis
import chess.pgn
import chess
import pickle
import signal
import numpy as np
from sklearn import linear_model, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt # 3.5.1
import pandas # 1.4.1

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

    # data["piece_counts"] =   analysis.get_piece_counts(board), 
    data["legal_moves"]  =   len(list(board.legal_moves)) * is_good
    data["game_depth"]  = len(board.move_stack)
    data['central_control'] = analysis.get_central_squares_control(board) * is_good
    # print('\t',data)
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
        
        # score['result']=won
        # print(score)
        results.append(score)

    return results

def add_plot_data(x, y, x_label="",y_label=""):
    plt.plot(x,y, 'o')
    if x_label != "":
        plt.xlabel(x_label)
    if y_label != "":
        plt.ylabel(y_label)
    return plt
    
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

    # with open("measurements.obj",'wb') as measurements_file:
    #         pickle.dump(measurements,measurements_file,-1)
    organized_chess_data = DataFrame(measurements)
    min_max_scaling = preprocessing.MinMaxScaler()
    cols = organized_chess_data.columns
    game_depth = organized_chess_data['game_depth']
    
    normalized_ocd = min_max_scaling.fit_transform(organized_chess_data.values)
    norm_ocd_df = DataFrame(normalized_ocd, columns=cols)
    # norm_ocd_df['game_depth'] = game_depth

    print(norm_ocd_df)
    LR = linear_model.LinearRegression()
   
    # with open("ocd.obj",'wb') as measurements_file:
    #     pickle.dump(ocd,measurements_file,-1)
    y_data = norm_ocd_df['game_depth']
    x_data = norm_ocd_df.drop('game_depth',axis=1)
    
    # norm_ocd_df.drop('winner')
    # x_train, x_test, y_train, y_test = train_test_split(x_data, y_data)#, test_size=0.3, random_state = 37)

    LR.fit(x_data,y_data)
    # y_pred = LR.predict(x_test)
    # r = r2_score(y_test, y_pred)
    # mse = mean_squared_error(y_test, y_pred)

    # print("r^2:               ", r)
    # print("mean square Error: ", mse)
    # 5 analyze Coefficients

    names=LR.feature_names_in_
    b = LR.intercept_
    m = LR.coef_
    model = {}
    i=0
    with open("ocd.obj",'wb') as measurements_file:
        pickle.dump((names,m,b),measurements_file,-1)
    for name in names:
        # print(name, m[i])
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

    
