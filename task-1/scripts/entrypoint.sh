#!/usr/bin/env bash

POSTGRES_HOST_AND_PORT=${POSTGRES_HOST_AND_PORT:-"postgres:5432"}
MAX_ATTEMPTS=30  # For example, a maximum of 30 attempts (3 seconds)
attempt_num=1

SEED_SCRIPT_PATH="/app/seed.py"

echo "Waiting for postgres to start..."
echo "Connections details: $POSTGRES_HOST_AND_PORT"

while ! nc -z $POSTGRES_HOST_AND_PORT; do
  sleep 0.1
  if [ $attempt_num -eq $MAX_ATTEMPTS ]; then
    echo "Timeout waiting for PostgreSQL at $POSTGRES_HOST_AND_PORT"
    exit 1
  fi
  echo "PostgreSQL not available yet, retrying ($attempt_num/$MAX_ATTEMPTS)..."
  ((attempt_num++))
done

echo "PostgreSQL started at $POSTGRES_HOST_AND_PORT"
echo "Running seed script..."

python ${SEED_SCRIPT_PATH}
exit $?
