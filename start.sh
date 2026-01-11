#!/bin/bash

echo "Initializing database..."
python db/init_db.py || true

echo "Starting FastAPI server..."
uvicorn api.main:app --host 0.0.0.0 --port $PORT
