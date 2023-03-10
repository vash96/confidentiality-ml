from concurrent import futures
import logging

from numpy import frombuffer, transpose
from numpy.linalg import norm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import grpc
import remote_ml_pb2_grpc
import remote_ml_pb2


"""
RemotePCA provides an implementation of the methods of the RemoteML service
under the Principal Component Analysis schema.
"""
class RemotePCAServicer(remote_ml_pb2_grpc.RemoteMLServicer):
    def __init__(self) -> None:
        self.training_matrix = None
        self.scaler = None
        self.principal_components = None
        self.principal_components_t = None

    def Train(self, array, context):
        training_matrix = frombuffer(array.data).reshape(array.shape)

        self.scaler = StandardScaler().fit(training_matrix)
        self.training_matrix = self.scaler.transform(training_matrix)

        self.principal_components = PCA().fit(training_matrix).components_
        self.principal_components_t = transpose(self.principal_components)

        return remote_ml_pb2.Empty()
    
    def FaultIndicator(self, array, context):
        test_matrix = frombuffer(array.data).reshape(array.shape)
    
        test_matrix = self.scaler.transform(test_matrix)

        residual = test_matrix - ((test_matrix @ self.principal_components_t) @ self.principal_components)
        residual = norm(residual)

        return remote_ml_pb2.Float(
            x = residual
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    remote_ml_pb2_grpc.add_RemoteMLServicer_to_server(
        RemotePCAServicer(),
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