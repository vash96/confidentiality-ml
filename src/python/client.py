import logging
import os

import grpc
import preservation_plugin_pb2_grpc
import preservation_plugin_pb2
import remote_ml_pb2_grpc
import remote_ml_pb2

from numpy import array_equal, frombuffer
from sklearn import datasets


def open_grpc_channel(service_name):
    logging.info(f"Connecting to {service_name}_SERVER.")

    port = os.environ.get(f"{service_name}_SERVER_PORT")

    if port is None:
        logging.error(f"{service_name}_SERVER_PORT does not exists!")
        raise ValueError(f"{service_name}_SERVER_PORT does not exists!")

    return grpc.insecure_channel(f"localhost:{port}")


def run():
    preservation_plugin = preservation_plugin_pb2_grpc.PreservationPluginStub(
        open_grpc_channel('PRESERVATION_PLUGIN')
    )

    logging.info("Preparing dataset iris.")
    iris = datasets.load_iris().data

    logging.info("Start interaction with PreservationPlugin (Scramble).")
    scrambled = preservation_plugin.Scramble(
        preservation_plugin_pb2.ToScramble(
            array = preservation_plugin_pb2.NDArray (
                data = iris.tobytes(),
                shape = iris.shape
            ),
            kind = preservation_plugin_pb2.COL
        )
    )

    logging.info("Getting scrambled data and used permutation.")
    scram = frombuffer(scrambled.array.data).reshape(scrambled.array.shape)
    perm = frombuffer(scrambled.perm.data)
    kind = scrambled.perm.kind

    logging.info("Start interaction with PreservationPlugin (DeScramble).")
    descrambled = preservation_plugin.DeScramble(
        preservation_plugin_pb2.Scrambled(
            array = preservation_plugin_pb2.NDArray(
                data = scram.tobytes(),
                shape = scram.shape
            ),
            perm = preservation_plugin_pb2.Permutation(
                data = perm.tobytes(),
                kind = kind
            )
        )
    )

    logging.info("Getting unscrambled data.")
    descram = frombuffer(descrambled.data).reshape(descrambled.shape)

    logging.info("Checking that 'original == de-scrambled'.")
    if array_equal(iris, descram):
        logging.info("Success! Scrambled/De-scrambled data correctly.")
    else:
        logging.error("Error! De-scrambled data is not correct. Could be either Scramble or DeScramble.")
        raise ValueError("Error! De-scrambled data is not correct. Could be either Scramble or DeScramble.")





    logging.info("Creating RemotePCA stub.")
    remote_pca = remote_ml_pb2_grpc.RemoteMLStub(
        open_grpc_channel('PCA')
    )

    logging.info("Training RemotePCA with iris dataset.")
    remote_pca.Train(
        remote_ml_pb2.NDArray(
            data = iris.tobytes(),
            shape = iris.shape
        )
    )

    logging.info("Testing RemotePCA FaultIndicator with original dataset.")
    original_fi = remote_pca.FaultIndicator(
        remote_ml_pb2.NDArray(
            data = iris.tobytes(),
            shape = iris.shape
        )
    )
    logging.info(f"Computed fault indicator = {original_fi}.")

    


    logging.info("Creating RemotePCA stub.")
    remote_svd = remote_ml_pb2_grpc.RemoteMLStub(
        open_grpc_channel('SVD')
    )

    logging.info("Training RemoteSVD with iris dataset.")
    remote_svd.Train(
        remote_ml_pb2.NDArray(
            data = iris.tobytes(),
            shape = iris.shape
        )
    )

    logging.info("Testing RemoteSVD FaultIndicator with original dataset.")
    original_fi = remote_svd.FaultIndicator(
        remote_ml_pb2.NDArray(
            data = iris.tobytes(),
            shape = iris.shape
        )
    )
    logging.info(f"Computed fault indicator = {original_fi}.")


    logging.info("Client testing is finished, bye bye!")





def head(mat, n=10):
    return mat[:n,]


def main():
    logging.basicConfig(level = logging.DEBUG)
    run()
    
     

if __name__ == "__main__":
    main()