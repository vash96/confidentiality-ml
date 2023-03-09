from numpy.random import permutation
from numpy import argsort

class PreservationPlugin:
    def scramble(self, data_matrix, cols_scramble = False):
        perm_size = data_matrix.shape[cols_scramble]
        perm = permutation(perm_size)
        
        if cols_scramble:
            scram_data_matrix = data_matrix[:, perm]
        else:
            scram_data_matrix = data_matrix[perm]
        
        return (scram_data_matrix, perm)


    def descramble(self, scram_data_matrix, perm, cols_scramble = False):
        perm = argsort(perm) # Get inverse permutation

        if cols_scramble:
            return scram_data_matrix[:, perm]
        else:
            return scram_data_matrix[perm]