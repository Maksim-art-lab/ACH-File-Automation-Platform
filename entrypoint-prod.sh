#! /usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:/app"

if [ "${POSTGRES_HOST}" != "localhost" ]; then
  (exec alembic --config server/alembic.ini upgrade head)
fi

gunicorn server.main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --timeout 60 --bind 0.0.0.0:8000 --log-level trace