from sklearn import decomposition
import sklearn


class RemoteML:
    def pca(self, data_matrix):
        return decomposition.PCA().fit(data_matrix)