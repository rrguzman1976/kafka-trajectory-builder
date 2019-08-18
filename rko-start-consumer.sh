#!/bin/bash -eux

echo "waiting for consumer..."
#sleep 2s

# TEST: Start survey consumer
# Unbuffer so that output is visible
docker-compose -f docker-compose-consumer.yml build
docker-compose -f docker-compose-consumer.yml run \
    --name python-survey-consumer \
    --rm \
    survey-consumer \
    python3.6 -u consume_dbz_well.py