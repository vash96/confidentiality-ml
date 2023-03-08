from os import environ
from sys import stderr
import logging

import Pyro5.api

import remote_ml

def main():
    # Logger
    logging.basicConfig(level = logging.DEBUG)

    # Choose server to run
    server_type = environ.get('REMOTE_ML_TYPE')

    match server_type:
        case 'PCA':
            server = remote_ml.RemotePCA()
        case 'SVD':
            server = remote_ml.RemotePCA()
        case _:
            logging.warning("Environment variable 'REMOTE_ML_TYPE' is not defined or has wrong value.")
            logging.warning("Available values: 'PCA' | 'SVD'.")
            logging.warning("Defaulted to 'PCA'.")
            server_type = 'PCA'
            server = remote_ml.RemotePCA()

    logging.info("Starting Pyro5.api.Daemon() routine.")
    # Exposing via Pyro5
    with Pyro5.api.Daemon() as daemon:
        logging.info("Registering uri of the server.")
        server_uri = daemon.register(server)
        with Pyro5.api.locate_ns() as name_server:
            logging.info("Locating Pyro5 nameserver.")
            name_server.register(f'confidentiality.remote_ml.{server_type}', server_uri)
        logging.info("Running daemon.requestLoop().")
        daemon.requestLoop()

if __name__ == "__main__":
    main()