import scraml
import numpy as np
from sklearn import datasets
from sklearn import decomposition

def main():
    iris = datasets.load_iris()
    data_matrix = iris.data
    print("Using Iris data matrix:\n\n{}\n\n"\
          .format(data_matrix[:10,]))
    scrambled, perm = scraml.scramble(data_matrix)

    print("Scramble matrix is:\n\n{}\n\n"\
          .format(scrambled[:10, ]))

    descrambled = scraml.descramble(scrambled, perm)
    print("Is de-scrambled == original? {}\n\n"\
          .format(np.array_equal(data_matrix, descrambled)))
    pass

if __name__ == "__main__":
    main()