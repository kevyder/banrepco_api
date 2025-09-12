#!/bin/bash
set -e

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 3000