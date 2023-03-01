import scraml
import remote_ml
import numpy as np
from sklearn import datasets
from sklearn import decomposition

def main():
    iris = datasets.load_iris()
    data_matrix = iris.data
    print("Using Iris data matrix:\n\n{}\n\n"\
          .format(data_matrix[:10,]))
    


    # Interaction with preservation plugin
    preservation_plugin = scraml.PreservationPlugin()

    scrambled, perm = preservation_plugin.scramble(data_matrix)
    print("Scramble matrix is:\n\n{}\n\n"\
          .format(scrambled[:10, ]))
    descrambled = preservation_plugin.descramble(scrambled, perm)
    print("Is de-scrambled == original? {}\n\n"\
          .format(np.array_equal(data_matrix, descrambled)))
    


    # Interaction with the remote_ml sever
    server = remote_ml.RemoteML()
    original_pc = server.pca(data_matrix)
    scrambled_pc = server.pca(scrambled)
    descrambled_pc = server.pca(descrambled)

if __name__ == "__main__":
    main()