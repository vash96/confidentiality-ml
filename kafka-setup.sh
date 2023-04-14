#!/bin/bash

KAFKA_DIR='bin/kafka_'$KAFKA_VERSION

pushd $KAFKA_DIR

bin/zookeeper-server-start.sh config/zookeeper.properties

popd