#!/bin/bash

set -e

# Environment variables are automatically loaded by Docker Compose
DB_NAME=${POSTGRES_DB}
DB_USER=${POSTGRES_USER}
DB_PASS=${POSTGRES_PASSWORD}
DB_PORT=5432

# Debug: Print all variables
echo "Debug: Environment variables:"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"
echo "DB_PORT: $DB_PORT"

# Ensure required variables are set
if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASS" || -z "$DB_PORT" ]]; then
  echo "Error: One or more required environment variables are not set."
  exit 1
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready on port $DB_PORT..."
until pg_isready -U postgres -p "$DB_PORT"; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
echo "PostgreSQL is ready."

# Debug: List backup directory contents
echo "Debug: Checking backup directory contents:"
ls -la /backup/

# Ensure the database exists
echo "Checking if database $DB_NAME exists on port $DB_PORT..."
DB_EXISTS=$(psql -U postgres -p "$DB_PORT" -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'")
if [[ "$DB_EXISTS" != "1" ]]; then
  echo "Database $DB_NAME does not exist. Creating..."
  createdb -U postgres -p "$DB_PORT" "$DB_NAME"
  echo "Database created."
fi

# Debug: Check database emptiness
echo "Debug: Checking if database is empty..."
DB_EMPTY=$(psql -U postgres -p "$DB_PORT" -d "$DB_NAME" -tAc "SELECT COUNT(*) = 0 FROM pg_tables WHERE schemaname = 'public';")
echo "Debug: DB_EMPTY value: $DB_EMPTY"

if [[ "$DB_EMPTY" == "t" ]]; then
  echo "Database $DB_NAME is empty. Attempting restore..."
  if [[ -f /backup/backup.sql ]]; then
    echo "Found backup file. Starting restore..."
    # Add error checking to the restore command
    if psql -U postgres -p "$DB_PORT" -d "$DB_NAME" < /backup/backup.sql; then
      echo "Restore completed successfully."
    else
      echo "Error: Restore failed!"
    fi
  else
    echo "Error: No backup file found at /backup/backup.sql"
  fi
else
  echo "Database $DB_NAME is not empty. Current tables:"
  psql -U postgres -p "$DB_PORT" -d "$DB_NAME" -c "\dt"
fi
