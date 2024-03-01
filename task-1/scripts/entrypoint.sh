#!/usr/bin/env bash

POSTGRES_DB=${POSTGRES_DB:-"task_manager"}
POSTGRES_USER=${POSTGRES_USER:-"db_admin"}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_HOST=${POSTGRES_HOST:-"postgres"}
POSTGRES_PORT=${POSTGRES_PORT:-"5432"}

MAX_ATTEMPTS=300  # For example, a maximum of 30 attempts (3 seconds)
attempt_num=1

SEED_SCRIPT_PATH="/app/seed.py"
SEED_SCRIPT_ARGS="--dbname ${POSTGRES_DB} --user ${POSTGRES_USER} --password ${POSTGRES_PASSWORD} --host ${POSTGRES_HOST} --port ${POSTGRES_PORT}"

echo "Waiting for postgres to start..."
echo "Connections details: ${POSTGRES_HOST}:${POSTGRES_PORT}"

while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  sleep 0.1
  if [[ ${attempt_num} -eq ${MAX_ATTEMPTS} ]]; then
    echo "Timeout waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}"
    exit 1
  fi
  echo "PostgreSQL not available yet, retrying (${attempt_num}/${MAX_ATTEMPTS})..."
  ((attempt_num++))
done

echo "PostgreSQL started at ${POSTGRES_HOST}:${POSTGRES_PORT}"
echo "Running seed script..."

python ${SEED_SCRIPT_PATH} ${SEED_SCRIPT_ARGS}
exit $?
