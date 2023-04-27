from pca_server import PCAServer

import logging

from sklearn import datasets
from numpy.random import choice as np_choice


def init_rand_servers(data, n_servers, rate):
    n_rows = data.shape[0]
    n_choice = int(n_rows * rate)
    servers = [PCAServer() for _ in range(n_servers)]
    
    for server in servers:
        random_choice = sorted(np_choice(n_rows, n_choice, replace=False))
        random_data = data[random_choice,]

        if rate < 0.10:
            logging.info(f"Random indeces [rate={rate}]: {random_choice}")
        server.train(random_data)
    
    return servers


def main():
    logging.info("Loading dataset 'iris'.\n")
    iris = datasets.load_iris().data

    n_rows, n_cols = iris.shape
    logging.info(f"Rows = {n_rows}")
    logging.info(f"Cols = {n_cols}\n")

    server_fulldata = PCAServer()
    server_fulldata.train(iris)

    rates = [.05, .10, .20, .50, .75]
    servers = { rate: init_rand_servers(data=iris, n_servers=10, rate=rate) for rate in rates}
    

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    main()