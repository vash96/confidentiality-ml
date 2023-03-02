from numpy import array_equal
from sklearn import datasets

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
    server_pca = remote_ml.RemotePCA()
    server_svd = remote_ml.RemoteSVD()

    # Playing with PCA
    server_pca.train(data_matrix)
    print("PCA fault-indicator of training set (should be close to 0):", server_pca.fault_indicator(data_matrix))


if __name__ == "__main__":
    main()