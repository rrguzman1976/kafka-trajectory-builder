#!/bin/bash -eux

# Shut down the cluster
export DEBEZIUM_VERSION=0.9

docker-compose down