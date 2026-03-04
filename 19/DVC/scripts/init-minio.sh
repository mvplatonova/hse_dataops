#!/bin/bash

# Скрипт для автоматического создания bucket в MinIO

set -e

echo "Waiting for MinIO to be ready..."
sleep 10

# MinIO credentials from environment
MINIO_HOST="${MINIO_HOST:-localhost:9000}"
MINIO_USER="${MINIO_ROOT_USER:-minioadmin}"
MINIO_PASSWORD="${MINIO_ROOT_PASSWORD:-minioadmin}"
BUCKET_NAME="${MINIO_LAKEFS_BUCKET:-lakefs-data}"

# Install mc if not present
if ! command -v mc &> /dev/null; then
    echo "Installing MinIO Client (mc)..."
    wget -q https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x mc
    sudo mv mc /usr/local/bin/ 2>/dev/null || mv mc /usr/bin/
fi

# Configure MinIO alias
echo "Configuring MinIO connection..."
mc alias set local http://${MINIO_HOST} ${MINIO_USER} ${MINIO_PASSWORD}

# Create bucket
echo "Creating bucket: ${BUCKET_NAME}"
mc mb local/${BUCKET_NAME} || echo "Bucket already exists"

# Set public policy (optional, for testing)
# mc anonymous set download local/${BUCKET_NAME}

# Verify bucket
echo "Verifying bucket..."
mc ls local/${BUCKET_NAME}

echo "✅ MinIO bucket '${BUCKET_NAME}' is ready!"
