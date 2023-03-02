from abc import ABC, abstractmethod
from numpy import transpose
from numpy.linalg import norm
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler


class RemoteML(ABC):
    @abstractmethod
    def train(self, training_matrix):
        # Scaling and centering
        self.training_matrix = StandardScaler().fit_transform(training_matrix)

    @abstractmethod
    def fault_indicator(self, test_matrix):
        pass


class RemotePCA(RemoteML):
    ## PRIVATE
    def _pca(self):
        return PCA().fit(self.training_matrix).components_
    
    ## PUBLIC
    def train(self, training_matrix):
        super().train(training_matrix)
        self.principal_components = self._pca()
        
    def fault_indicator(self, test_matrix):
        return norm(
            test_matrix - ((test_matrix @ transpose(self.principal_components)) @ self.principal_components)
        )
    


class RemoteSVD(RemoteML):
    ## PRIVATE
    def _svd(self):
        return TruncatedSVD().fit(self.training_matrix).singular_values_
    
    ## PUBLIC
    def train(self, training_matrix):
        super().train(training_matrix)
        self.singular_values = self._svd()

    def fault_indicator(self, test_matrix):
        return 69
