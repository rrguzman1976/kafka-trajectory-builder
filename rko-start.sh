#!/bin/bash -eux

# Start the topology as defined in http://debezium.io/docs/tutorial/
export DEBEZIUM_VERSION=0.9
docker-compose build
docker-compose up -d

echo "waiting for SQL..."
sleep 15s

# Initialize database and insert test data
cat debezium-mssql-init/create-db.sql | \
    docker exec -i kafka-trajectory-builder_sqlserver_1 bash \
    -c '/opt/mssql-tools/bin/sqlcmd -U sa -P $SA_PASSWORD'

# Start SQL Server connector
# topic created: funky-chicken.dbo.Well
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
    http://localhost:8083/connectors/ -d @debezium-mssql-init/register-sqlserver.json

# Create topics
# Input topic
docker-compose exec kafka /kafka/bin/kafka-topics.sh \
    --zookeeper zookeeper:2181 \
    --topic dir-survey-01 \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --config cleanup.policy=compact

# Output topic 1: stream survey counts per API
docker-compose exec kafka /kafka/bin/kafka-topics.sh \
    --zookeeper zookeeper:2181 \
    --topic dir-survey-counts-01 \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --config cleanup.policy=compact

# Output topic 2: reduce survey by max GC per API
docker-compose exec kafka /kafka/bin/kafka-topics.sh \
    --zookeeper zookeeper:2181 \
    --topic dir-survey-max-02 \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --config cleanup.policy=compact