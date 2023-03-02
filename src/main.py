from numpy import array_equal
from sklearn import datasets
from sklearn import decomposition

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
    


    # Interaction with the remote_ml sever
    server = remote_ml.RemoteML()

    # Playing with PCA
    original_pc = server.pca(data_matrix)
    scrambled_pc = server.pca(scrambled)
    descrambled_pc = server.pca(descrambled)

    print("{}\n{}\n{}\n\n".format(original_pc, scrambled_pc, descrambled_pc))

    # Playing with SVD
    original_s = server.svd(data_matrix)
    scrambled_s = server.svd(scrambled)
    descrambled_s = server.svd(descrambled)

    print("{}\n{}\n{}\n\n".format(original_s, scrambled_s, descrambled_s))


if __name__ == "__main__":
    main()