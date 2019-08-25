#!/bin/bash -eux

# Start the topology as defined in http://debezium.io/docs/tutorial/
export DEBEZIUM_VERSION=0.9
docker-compose -f docker-compose-kafka.yml build
docker-compose -f docker-compose-kafka.yml up -d

echo "waiting for SQL..."
sleep 25s

# Initialize database and insert test data
cat debezium-mssql-init/create-db.sql | \
    docker exec -i kafka-trajectory-builder_mssql_1 bash \
    -c '/opt/mssql-tools/bin/sqlcmd -U sa -P $SA_PASSWORD'

echo "waiting for SQL CDC..."
sleep 5s

# Start SQL Server connector
# topic created: funky-chicken.dbo.Well
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
    http://localhost:8083/connectors/ -d @debezium-mssql-init/register-sqlserver.json

# Create topics
# Input topic
docker-compose -f docker-compose-kafka.yml exec kafka \
    /kafka/bin/kafka-topics.sh \
    --zookeeper zookeeper:2181 \
    --topic survey-acq \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --config cleanup.policy=compact

# Output topic 1: enrich topic with API
docker-compose -f docker-compose-kafka.yml \
    exec kafka /kafka/bin/kafka-topics.sh \
    --zookeeper zookeeper:2181 \
    --topic survey-cln \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --config cleanup.policy=compact
