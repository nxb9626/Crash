"""
Runs an adaptation server, which receives data from the bot and determines if 
changes should be made for its decision making
"""
import pickle

with open("ocd.obj",'rb') as measurements_file:
    names, m, b = pickle.load(measurements_file)
    print(names)
    print(m)
    
def adapt(scores,weights):
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    moves = weights['move_count'] + weights['max_depth']
    i = 0
    while i < len(names):
        scores[names[i]] = scores[names[i]] * ((m[i] * moves) + b)
        i+=1
    return scores
