from ml_server import MLServer

from numpy import transpose
from numpy.linalg import norm
from sklearn.decomposition import PCA

class PCAServer(MLServer):
    # PRIVATE

    def _failure_indicator(self, test_data) -> float:
        error = test_data - ((test_data @ self.princomp_t) @ self.princomp)
        return norm(error)



    # PUBLIC

    def train(self, training_data, n_comps = None) -> None:
        super().train(training_data)

        if n_comps is None:
            n_comps = training_data.shape[1]

        self.princomp   = PCA().fit(self.training_data).components_[:n_comps]
        self.princomp_t = transpose(self.princomp)