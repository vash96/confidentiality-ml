from concurrent import futures
import logging

from numpy.random import permutation
from numpy import argsort, frombuffer

import grpc
import preservation_plugin_pb2_grpc
import preservation_plugin_pb2
from preservation_plugin_pb2 import ScrambleKind


# PreservationPluginServicer provides an implementation of the methods of the PreservationPlugin service
class PreservationPluginServicer(preservation_plugin_pb2_grpc.PreservationPluginServicer):
    def Scramble(self, to_scramble, context):
        array = frombuffer(to_scramble.array.data).reshape(to_scramble.array.shape)
        kind = to_scramble.kind
        
        logging.debug(f"{ScrambleKind.Value('ROW')}")

        logging.info(f"Started scrambling operation of kind {kind}.")

        perm_size = array.shape[kind]
        perm = permutation(perm_size)
        
        logging.info(f"Got random permutation of size {perm_size}.")

        if kind == ScrambleKind.Value('ROW'):
            scram = array[perm]
        elif kind == ScrambleKind.Value('COL'):
            scram = array[:, perm]
        else:
            logging.error(f"Kind {kind} is not supported yet.")
            raise ValueError(f"Kind {kind} is not supported yet.")
        
        return preservation_plugin_pb2.Scrambled(
            array = preservation_plugin_pb2.NDArray (
                data = scram.tobytes(),
                shape = scram.shape
            ),
            perm = preservation_plugin_pb2.Permutation (
                data = perm.tobytes(),
                kind = kind
            )
        )

    def DeScramble(self, scrambled, context):
        array = frombuffer(scrambled.array.data).reshape(scrambled.array.shape)
        perm = frombuffer(scrambled.perm.data)
        kind = scrambled.perm.kind


        logging.info(f"Started de-scrambling operation of kind {kind}.")

        logging.info("Got inverse permutation.")
        perm = argsort(perm) # Get inverse permutation

        if kind == ScrambleKind.Value('ROW'):
            array = array[perm]
        elif kind == ScrambleKind.Value('COL'):
            array = array[:, perm]
        else:
            logging.error(f"Kind {kind} is not supported yet.")
            raise ValueError(f"Kind {kind} is not supported yet.")
        
        return preservation_plugin_pb2.NDArray (
            data = array.tobytes(),
            shape = array.shape
        )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    preservation_plugin_pb2_grpc.add_PreservationPluginServicer_to_server(
        PreservationPluginServicer(),
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