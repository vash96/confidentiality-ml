from numpy import array_equal
from sklearn import datasets
from os import environ
from sys import stderr

import scraml
import remote_ml

def head(mat, n=10):
    return mat[:n,]

def main():
    iris = datasets.load_iris()
    data_matrix = iris.data
    print("Using Iris data matrix:\n{}\n    .........\nWith {} observations over {} features.\n"\
          .format(head(data_matrix), data_matrix.shape[0], data_matrix.shape[1]))
    


    # Interaction with preservation plugin
    preservation_plugin = scraml.PreservationPlugin()

    scrambled, perm = preservation_plugin.scramble(data_matrix)
    print("Scrambled matrix:\n{}\n    .........\n"\
          .format(head(scrambled)))
    descrambled = preservation_plugin.descramble(scrambled, perm)
    print("Is de-scrambled == original? {}\n\n"\
          .format(array_equal(data_matrix, descrambled)))
    


    # Interaction with the remote_ml severs
    # Choose server to run

    server_type = environ.get('REMOTE_ML_TYPE')
    if server_type is None:
        print("Warning! Env variable 'REMOTE_ML_TYPE' does not exists and is defaulted to 'REMOTE_ML_TYPE=PCA'.", file = stderr)
        server_type = 'PCA'

    if server_type == 'PCA':
        server = remote_ml.RemotePCA()
    else:
        server = remote_ml.RemoteSVD()

    server.train(data_matrix)
    print(f"Fault indicator = {server.fault_indicator(data_matrix)}")


if __name__ == "__main__":
    main()