import pickle
import numpy as np
np.set_printoptions(precision=5)
with open("ocd.obj",'rb') as measurements_file:
    names,m,b = pickle.load(measurements_file)
    i=0
    while i < len(names):
        print(names[i],m[i])
        i+=1
    # print(names)
    # print(m)
