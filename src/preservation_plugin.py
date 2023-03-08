import logging

import Pyro5.api

import scraml

def main():
    # Logger
    logging.basicConfig(level = logging.DEBUG)

    preservation_plugin = scraml.PreservationPlugin()

    logging.info("Starting Pyro5.api.Daemon() routine.")
    # Exposing via Pyro5
    with Pyro5.api.Daemon() as daemon:
        logging.info("Registering uri of the preservation_plugin.")
        server_uri = daemon.register(preservation_plugin)
        with Pyro5.api.locate_ns() as name_server:
            logging.info("Locating Pyro5 nameserver.")
            name_server.register(f'confidentiality.preservation_plugin', server_uri)
        logging.info("Running daemon.requestLoop().")
        daemon.requestLoop()

if __name__ == "__main__":
    main()