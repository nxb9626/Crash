import pickle
import numpy as np
import matplotlib.pyplot as plt 

np.set_printoptions(precision=2)
with open("ocd.obj",'rb') as measurements_file:
    names,m,b = pickle.load(measurements_file)
    i=0
    hundo = [i for i in range(0,100)]
    while i < len(names):
        name,coef = names[i],m[i]
        # print(name, coef)
        if name not in {'k','b','n','r','q','p','K','B','N','R','P','Q'}:
            # print(name)
            i+=1
            continue
        i+=1
        line = []
        for x in hundo:
            line.append(coef*x + b)
        print(line)
        plt.plot(hundo, line,label=str(name))

    # print(names)
    # print(m)
    
    x_label = 'game_depth'
    
    y_label = 'central_control'
    
    
    plt.xlabel(x_label)
    plt.show()
