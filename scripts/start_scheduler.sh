#!/bin/bash
set -e

echo "Starting scheduler..."
exec python -m src.jobs.scheduler
