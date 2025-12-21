#!/bin/bash

# Get the script's directory and set up paths relative to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BACKUP_DIR="$SCRIPT_DIR/../backup"
DUMP_DIR="$BACKUP_DIR/dumps"
LOG_DIR="$BACKUP_DIR/logs"

# Create directories
mkdir -p "$BACKUP_DIR"
mkdir -p "$DUMP_DIR"
mkdir -p "$LOG_DIR"

# Set up logging
exec 1> >(tee -a "${LOG_DIR}/backup_$(date +%Y%m%d).log")
exec 2>&1

echo "=== Backup started at $(date) ==="

# Load only the POSTGRES_PASSWORD from the .env file
ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file not found at $ENV_FILE"
    exit 1
fi

# Extract POSTGRES_PASSWORD safely
POSTGRES_PASSWORD=$(grep '^POSTGRES_PASSWORD=' "$ENV_FILE" | cut -d '=' -f2- | tr -d '"' | xargs)

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Error: POSTGRES_PASSWORD not set or could not be read from environment file"
    exit 1
fi

# Generate timestamp and filename
TIMESTAMP=$(date +%Y%m%d)
BACKUP_FILE="$DUMP_DIR/onaylfdjango$TIMESTAMP.sql"

# Create the backup
echo "Creating backup file: $BACKUP_FILE"
docker exec -i onaylf_postgres /bin/bash -c "PGPASSWORD=$POSTGRES_PASSWORD pg_dump --username postgres onaylfdjango" > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
    echo "Backup size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "Error: Backup failed"
    exit 1
fi

# Rotate old backups
echo "Starting backup rotation..."
find "$DUMP_DIR" -name "onaylfdjango*.sql" -type f | while read file; do
    filedate=$(basename "$file" | sed 's/onaylfdjango\([0-9]\{8\}\)\.sql/\1/')
    age=$(( ( $(date +%s) - $(date -d "$filedate" +%s) ) / 86400 ))
    
    if [ $age -le 30 ]; then
        continue
    elif [ $age -le 365 ]; then
        day_of_month=$(date -d "$filedate" +%d)
        if [[ "$day_of_month" =~ ^(01|08|15|22|29)$ ]]; then
            continue
        fi
    else
        day_of_month=$(date -d "$filedate" +%d)
        if [ "$day_of_month" = "01" ]; then
            continue
        fi
    fi
    
    echo "Removing old backup: $file"
    rm "$file"
done
