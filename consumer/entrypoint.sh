#!/bin/sh

while ! kafkacat -b kafka:9092 -L; do
    echo "Waiting for Kafka to be ready..."
    sleep 1
done

echo "Kafka is ready - executing command"

exec "$@"