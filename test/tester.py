from pca_server import PCAServer

import logging

from sklearn import datasets
from pandas import read_csv
from numpy import arange, log
from numpy.random import choice as np_choice
from matplotlib import pyplot as plt


def init_rand_servers(data, n_servers, rate):
    n_rows = data.shape[0]
    n_choice = int(n_rows * rate)
    servers = [PCAServer() for _ in range(n_servers)]
    
    for server in servers:
        random_choice = sorted(np_choice(n_rows, n_choice, replace=False))
        random_data = data[random_choice,]

        server.train(random_data)
    
    return servers

def init_segmented_servers(data, rate, disjoint=True):
    n_rows = data.shape[0]
    length = int(n_rows * rate)
    n_servers = n_rows // length
    servers = [PCAServer() for _ in range(n_servers)]

    # Disjoint windows of data vs. random starting points (possible overlap of data)
    if disjoint:
        starting_points = [i*length for i in range(n_servers)]
    else:
        starting_points = sorted(np_choice(n_rows-length, n_servers, replace=False))

    for i in range(n_servers):
        starting_point = starting_points[i]
        window = data[starting_point:starting_point+length+1, ]

        servers[i].train(window)

    return servers


def generic_test_routine(test_data, servers):
    avg_errors = []

    for rate in servers.keys():
        logging.info(f"Testing servers with rate {rate}. Failure indicators per server:")
        avg_error = 0.0
        for server in servers[rate]:
            fi = server.failure_indicator(test_data)
            avg_error += fi
            logging.info(f"-- {fi}")
        avg_error /= len(servers[rate])
        avg_errors.append(avg_error)
        logging.info("\n")
        logging.info(f"Average error: {avg_error}.\n")
        logging.info(f"Average log(error): {log(avg_error)}.\n")
    
    return avg_errors


def test_running_condition(running_condition, servers):
    logging.info("\nTest 1: this test should produce SMALL values of failure (dataset is from running condition).\n")

    return generic_test_routine(running_condition, servers)

def test_failure_condition(failure_condition, servers):
    logging.info("\nTest 2: this test should produce LARGE values of failure (dataset is from failure condition).\n")
    
    return generic_test_routine(failure_condition, servers)


def prepare_dataset():
    dataset = read_csv("../datasets/felipe_clean.csv")

    ok_condition = dataset[dataset["Critical"] == False].drop(columns=["Critical"])
    fail_condition = dataset[dataset["Critical"] == True].drop(columns=["Critical"])

    return ok_condition.to_numpy(), fail_condition.to_numpy()


def main():
    logging.info("Preparing optical dataset.\n")
    ok_condition, fail_condition = prepare_dataset()


    n_rows, n_cols = ok_condition.shape
    logging.info(f"Shape of 'ok_condition': {ok_condition.shape}")
    logging.info(f"Shape of 'fail_condition': {fail_condition.shape}")

    """
    Create PCA servers:
        - Trained with full dataset (1 server)
        - Trained with 'rate' size of the dataset (10 for each rate)
    """
    server_fulldata = PCAServer()
    server_fulldata.train(ok_condition)

    logging.info("Principal components of training:")
    logging.info(server_fulldata.get_pc())

    rates = [.01, .02, .03, .04, .05, .10, .20, .50, .75]
    servers = { rate: init_rand_servers(data=ok_condition, n_servers=10, rate=rate) for rate in rates }
    servers[1.0] = [server_fulldata]

    avg_errors_1 = test_running_condition(ok_condition, servers)
    avg_errors_2 = test_failure_condition(fail_condition, servers)
    ratios = [err_1 / err_2 for err_1, err_2 in zip(avg_errors_1, avg_errors_2)]

    logging.info("=========================")
    logging.info("Summary:")
    logging.info(f"Test 1: errors should be SMALL. Average errors per rate:\n{avg_errors_1}")
    logging.info(f"Test 2: errors should be LARGE. Average errors per rate:\n{avg_errors_2}")
    logging.info(f"Relative comparisons:\n{ratios}")


    plt.style.use("ggplot")
    fig, axs = plt.subplots(3)

    axs[0].plot(rates + [1.0], avg_errors_1, label="avg FI from running cond.", color="green")
    axs[0].plot(rates + [1.0], avg_errors_2, label="avg FI from failure cond.", color="red")
    axs[0].legend(loc = "center right")
    axs[0].set_title("Training from randomly chosen rows.")

    logging.info("========================")
    logging.info("TRAINING FROM CONTIGUOUS AND DISJOINT DATA WINDOWS")
    servers = {}
    servers = { rate: init_segmented_servers(data=ok_condition, rate=rate) for rate in rates }
    servers[1.0] = [server_fulldata]

    avg_errors_1 = test_running_condition(ok_condition, servers)
    avg_errors_2 = test_failure_condition(fail_condition, servers)
    ratios = [err_1 / err_2 for err_1, err_2 in zip(avg_errors_1, avg_errors_2)]

    logging.info("=========================")
    logging.info("Summary:")
    logging.info(f"Test 1: errors should be SMALL. Average errors per rate:\n{avg_errors_1}")
    logging.info(f"Test 2: errors should be LARGE. Average errors per rate:\n{avg_errors_2}")
    logging.info(f"Relative comparisons:\n{ratios}")

    axs[1].plot(rates + [1.0], avg_errors_1, label="avg FI from running cond.", color="green")
    axs[1].plot(rates + [1.0], avg_errors_2, label="avg FI from failure cond.", color="red")
    axs[1].legend(loc="center right")
    axs[1].set_title("Training from disjoint 'windows' of data-rows.")

    logging.info("========================")
    logging.info("TRAINING FROM CONTIGUOUS AND RANDOM STARTING DATA WINDOWS")
    servers = {}
    servers = { rate: init_segmented_servers(data=ok_condition, rate=rate, disjoint=False) for rate in rates }
    servers[1.0] = [server_fulldata]

    avg_errors_1 = test_running_condition(ok_condition, servers)
    avg_errors_2 = test_failure_condition(fail_condition, servers)
    ratios = [err_1 / err_2 for err_1, err_2 in zip(avg_errors_1, avg_errors_2)]

    logging.info("=========================")
    logging.info("Summary:")
    logging.info(f"Test 1: errors should be SMALL. Average errors per rate:\n{avg_errors_1}")
    logging.info(f"Test 2: errors should be LARGE. Average errors per rate:\n{avg_errors_2}")
    logging.info(f"Relative comparisons:\n{ratios}")

    axs[2].plot(rates + [1.0], avg_errors_1, label="avg FI from running cond.", color="green")
    axs[2].plot(rates + [1.0], avg_errors_2, label="avg FI from failure cond.", color="red")
    axs[2].legend(loc="center right")
    axs[2].set_title("Training from 'windows' of data-rows with random starting positions.")

    plt.show()
    

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    main()