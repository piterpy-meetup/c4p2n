#!/bin/sh

WORKERS_NUM=${1:-1}
PORT=${2:-8000}

exec 2>&1 gunicorn c4p2n.api:app --workers=$WORKERS_NUM --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT
