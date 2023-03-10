from concurrent import futures
import logging

from numpy import frombuffer, vstack
from numpy.linalg import norm
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

import grpc
import remote_ml_pb2_grpc
import remote_ml_pb2


"""
RemoteSVD provides an implementation of the methods of the RemoteML service
under the Singular Value Decomposition schema.
"""
class RemoteSVDServicer(remote_ml_pb2_grpc.RemoteMLServicer):
    ## PRIVATE
    def _svd(self, data_matrix):
        return TruncatedSVD().fit(data_matrix).singular_values_

    def _ith_fault_indicator(self, observation):
        # vstack is used as 'vertical stack', i.e., observation row is added to training_matrix
        singular_values = self._svd(vstack([self.training_matrix, observation]))
        return norm(self.singular_values - singular_values)
    

    ## PUBLIC
    def __init__(self) -> None:
        self.training_matrix = None
        self.scaler = None
        self.singular_values = None

    def Train(self, array, context):
        training_matrix = frombuffer(array.data).reshape(array.shape)

        self.scaler = StandardScaler().fit(training_matrix)
        self.training_matrix = self.scaler.transform(training_matrix)

        self.singular_values = self._svd(self.training_matrix)

        return remote_ml_pb2.Empty()
    
    def FaultIndicator(self, array, context):
        test_matrix = frombuffer(array.data).reshape(array.shape)
    
        test_matrix = self.scaler.transform(test_matrix)

        residual = sum(map(self._ith_fault_indicator, test_matrix))

        return remote_ml_pb2.Float(
            x = residual
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    remote_ml_pb2_grpc.add_RemoteMLServicer_to_server(
        RemoteSVDServicer(),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
            





def main():
    logging.basicConfig(level = logging.DEBUG)
    serve()


if __name__ == "__main__":
    main()