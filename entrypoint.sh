#!/bin/sh
set -e

echo "Waiting for db mount to be ready..."
until [ -f /code/db/data.db ]; do
  echo "data.db not found yet, retrying..."
  sleep 1
done

echo "Seeding credentials..."
python -m internal.utils.seed_credential

echo "Starting server..."
exec "$@"