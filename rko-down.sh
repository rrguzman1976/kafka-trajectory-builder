#!/bin/bash -eux

# Shut down the cluster
export DEBEZIUM_VERSION=0.9

docker-compose down
docker container prune -f
docker image prune -f
