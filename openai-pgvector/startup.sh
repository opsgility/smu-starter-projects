#!/bin/bash
cd /workspace
pip install -r requirements.txt -q 2>&1 | tail -3

# Initialize PostgreSQL if not already running
if ! pg_isready -q 2>/dev/null; then
    echo "Starting PostgreSQL..."
    service postgresql start 2>/dev/null || true
fi

# Create the database if it doesn't exist
psql -U postgres -c "CREATE DATABASE embeddings_db;" 2>/dev/null || true

echo "Environment ready. Run: python main.py"
