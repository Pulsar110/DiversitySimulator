import numpy as np

'''
    Input `neigh_vector` are vectors of type counts. 
'''

def TypeCountUtility(neigh_vector: np.array):
    '''
        Count the number of different types in the neighborhood.
    '''
    return len([i for i in neigh_vector if i > 0])