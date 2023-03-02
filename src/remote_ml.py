from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler


class RemoteML:
    def pca(self, data_matrix):
        # Scaling and centering
        data_matrix = StandardScaler().fit_transform(data_matrix)

        # Return principal components of data_matrix
        return PCA().fit(data_matrix).components_
        
    def svd(self, data_matrix):
        # Scaling and centering
        data_matrix = StandardScaler().fit_transform(data_matrix)

        # Return vector of singular values
        return TruncatedSVD().fit(data_matrix).singular_values_
