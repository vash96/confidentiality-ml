# SCRAML

Confidentiality-preserving Machine Learning techniques based on scam(b)ling.

## Objective

To implement and test the Preservation Plugin module sketched in Fig. 3 of [1].

## Technical details

The code is mainly written in Python and is located in `src/python/`.

There are four main modules:
- `preservation_plugin_server.py`: implements a server for (de-)scrambling service.
- `pca_server.py`: implements a server that simulates an external Fault Indicator service (see [1]) based on Principal Component Analysis.
- `svd_server.py`: implements a server that simulates an external Fault Indicator service (see [1]) based on Singular Values Decomposition.
- `client.py`: implements an hypothetical user that wants to interact with (de-)scrambling, PCA and SVD services.

The communication between the different components is done via [gRPC](https://grpc.io/) which should offer better performance (in terms of latency and data-throughput)
with respect to REST. For a comparison, see [here](https://medium.com/sahibinden-technology/benchmarking-rest-vs-grpc-5d4b34360911), [here](https://dev.to/stevenpg/grpc-vs-rest-simple-performance-test-228m)
and [here](https://blog.dreamfactory.com/grpc-vs-rest-how-does-grpc-compare-with-traditional-rest-apis/#:~:text=%E2%80%9CgRPC%20is%20roughly%207%20times,HTTP%2F2%20by%20gRPC.%E2%80%9D).

Proto files for the gRPC are located in `src/proto`.


## How to demo (using bash)

Run `env_vars.sh` script to make ports available from pyscripts.
```console
chmod +x env_vars.sh
source env_vars.sh
```

Run each server on a separate shell.
```console
python src/python/preservation_plugin_server.py
python src/python/pca_server.py
python src/python/svd_server.py
```

Run client on a separate shell.
```console
python src/python/client.py
```

The client will do the following:
- Load the `iris` dataset.
- Send `iris` to `PreservationPluginServer` and obtain `scrambled` dataset.
- Send `scrambled` to `PreservationPluginServer` and obtain `descrambled` dataset.
- Check that `iris` and `descrambled` are equal.
- Send `iris` to `RemotePCA` to train the model.
- Send `scrambled` to `RemotePCA` and obtain its fault indicator.
- Send `iris` to `RemoteSVD` to train the model.
- Send `scrambled` to `RemoteSVD` and obtain is fault indicator.


## Docker-containers

Alternatively, it is possible to build three docker images (one for each server).
```console
# Sometimes sudo is needed
docker build --tag preservation-plugin:latest -f docker_preservation_plugin.Dockerfile .
docker build --tag remote-pca:latest -f docker_pca.Dockerfile .
docker build --tag remote-svd:latest -f docker_svd.Dockerfile .
```

And run containers with port-mapping. Again, use `env_vars.sh`.
```console
chmod +x env_vars.sh
source env_vars.sh

# Docker-images expose (internal) port 50051
docker run --detach -p ${PRESERVATION_PLUGIN_SERVER_PORT}:50051 preservation-plugin
docker run --detach -p ${PCA_SERVER_PORT}:50051 remote-pca
docker run --detach -p ${SVD_SERVER_PORT}:50051 remote-svd
```

Again, run `src/python/client.py` to get a demo.


## TODO-list

- Testing
- Factor-Analysis server
- Multi-stage build of docker-images (space-efficiency)

## References

[1] M. Silva, A. Pacini, A. Sgambelluri, F. Paolucci, and L. Valcarenghi, "Confidentiality-preserving Machine Learning Scheme to Detect Soft-failures in Optical Communication Networks," in European Conference on Optical Communication (ECOC) 2022, J. Leuthold, C. Harder, B. Offrein, and H. Limberger, eds., Technical Digest Series (Optica Publishing Group, 2022), paper Tu3B.5.