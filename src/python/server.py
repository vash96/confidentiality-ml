from os import environ
from sys import stderr
import logging

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


if __name__ == "__main__":
    main()