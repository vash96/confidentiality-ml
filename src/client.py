import logging

from numpy import array_equal
from sklearn import datasets
import Pyro5.api


def head(mat, n=10):
    return mat[:n,]



def find_preservation_plugin():
    # Search from name_server
    with Pyro5.api.locate_ns() as name_server:
        logging.info("Searching for preservation_plugin.")
        preservation_plugin_uri = name_server.lookup("confidentiality.preservation_plugin")

    # Check existence
    if preservation_plugin_uri is None:
        logging.error("preservation_plugin not found!")
        raise ValueError("No preservation_plugin found! Check if it is running.")
    else:
        logging.info("preservation_plugin found!")

    return Pyro5.api.Proxy(preservation_plugin_uri)
        

def find_remote_ml_servers():
    # Search from name_server
    with Pyro5.api.locate_ns() as name_server:
        logging.info("Searching for remote_ml servers.")
        servers = []
        for server, server_uri in name_server.list(prefix="confidentiality.remote_ml.").items():
            logging.info(f"Found 'remote_ml.{server}'!")
            servers.append(Pyro5.api.Proxy(server_uri))
        
    # Check existence
    if not servers:
        logging.error("No remote_ml servers found.")
        raise ValueError("No remote_ml servers found! Check if they are running.")
    else:
        logging.info(f"Found servers.")
    
    return servers


def play(preservation_plugin, servers):
    logging.info("Start playing with remote objects.")

    server = servers[0]

    logging.info("Loading 'iris' dataset.")
    iris = datasets.load_iris()
    data_matrix = iris.data
    row, col = data_matrix.shape
    logging.info(f"Iris data matrix:\n{head(data_matrix)}\n    .........\nWith {row} observations over {col} features.\n")

    logging.info("Scrambling.")
    scrambled, perm = preservation_plugin.scramble(data_matrix)
    logging.info(f"Scrambled matrix:\n{head(scrambled)}\n    .........\n")

    logging.info("De-scrambling.")
    descrambled = preservation_plugin.descramble(scrambled, perm)
    logging.info(f"Is de-scrambled == original? {array_equal(data_matrix, descrambled)}\n\n")




def main():
    logging.basicConfig(level = logging.DEBUG)

    # Get remote Pyro5 objects
    logging.info("Searching for preservation_plugin and remote_ml servers.")
    preservation_plugin = find_preservation_plugin()
    servers = find_remote_ml_servers()

    logging.info("Found preservation_plugin and remote_ml servers.")

    # Start playing with remote objects
    play(preservation_plugin, servers)
    

if __name__ == "__main__":
    main()