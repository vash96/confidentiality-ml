FROM mambaorg/micromamba:1-bullseye-slim
LABEL name="RemotePCAServer"
LABEL version="1.0"
LABEL description="Implements an hypothetic server that does PCA."

COPY --chown=$MAMBA_USER:$MAMBA_USER remote_ml_environ.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml && \
    micromamba clean --all --yes

# (otherwise python will not be found)
ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV MAIN_NAME pca_server
ENV APP_HOME /${MAIN_NAME}
ENV PROTO_DIR ${APP_HOME}/proto
ENV PYTHON_DIR ${APP_HOME}/python

# Copy Proto
COPY src/proto/basic_types.proto ${PROTO_DIR}/basic_types.proto
COPY src/proto/remote_ml.proto ${PROTO_DIR}/remote_ml.proto

# Copy Python
COPY src/python/${MAIN_NAME}.py ${PYTHON_DIR}/${MAIN_NAME}.py

# Proto-compilation
USER root
RUN python3 -m grpc_tools.protoc \
    --proto_path=${PROTO_DIR} \
    --python_out=${PYTHON_DIR} \
    --pyi_out=${PYTHON_DIR} \
    --grpc_python_out=${PYTHON_DIR} \
    ${PROTO_DIR}/*.proto \
    && chown -R ${MAMBA_USER}:${MAMBA_USER} ${APP_HOME}
USER ${MAMBA_USER}

ENV PCA_SERVER_PORT 50051
EXPOSE ${PCA_SERVER_PORT}

CMD python ${PYTHON_DIR}/${MAIN_NAME}.py