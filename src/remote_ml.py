from abc import ABC, abstractmethod
from numpy import vstack, transpose
from numpy.linalg import norm
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
import Pyro5.api


@Pyro5.api.behavior(instance_mode="single")
class RemoteML(ABC):
    @abstractmethod
    def train(self, training_matrix):
        # Scaling and centering
        self.scaler = StandardScaler().fit(training_matrix)
        self.training_matrix = self.scaler.transform(training_matrix)

    @abstractmethod
    def fault_indicator(self, test_matrix):
        test_matrix = self.scaler.transform(test_matrix)
        return test_matrix


@Pyro5.api.expose
class RemotePCA(RemoteML):
    ## PUBLIC
    def train(self, training_matrix):
        super().train(training_matrix)
        self.principal_components = PCA().fit(training_matrix).components_
        self.principal_components_t = transpose(self.principal_components)
        
    def fault_indicator(self, test_matrix):
        test_matrix = super().fault_indicator(test_matrix)
        residual = test_matrix - ((test_matrix @ self.principal_components_t) @ self.principal_components)
        return norm(residual)
    


@Pyro5.api.expose
class RemoteSVD(RemoteML):
    ## PRIVATE
    def _svd(self, data_matrix):
        return TruncatedSVD().fit(data_matrix).singular_values_

    def _ith_fault_indicator(self, observation):
        # vstack is used as 'vertical stack', i.e., observation row is added to training_matrix
        singular_values = self._svd(vstack([self.training_matrix, observation]))
        return norm(self.singular_values - singular_values)

    ## PUBLIC
    def train(self, training_matrix):
        super().train(training_matrix)
        self.singular_values = self._svd(self.training_matrix)

    def fault_indicator(self, test_matrix):
        test_matrix = super().fault_indicator(test_matrix)
        return sum(map(self._ith_fault_indicator, test_matrix))