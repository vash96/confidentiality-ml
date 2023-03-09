import logging

import grpc
import preservation_plugin_pb2_grpc
import preservation_plugin_pb2

from numpy import array_equal, frombuffer
from sklearn import datasets



def run():
    logging.info("Connect to PreservationPlugin client.")
    with grpc.insecure_channel('localhost:50051') as channel:
        preservation_plugin = preservation_plugin_pb2_grpc.PreservationPluginStub(channel)

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

    logging.info("Client testing is finished, bye bye!")





def head(mat, n=10):
    return mat[:n,]


def main():
    logging.basicConfig(level = logging.DEBUG)
    run()
    
     

if __name__ == "__main__":
    main()