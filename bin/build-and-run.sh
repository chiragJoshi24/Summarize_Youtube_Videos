#!/bin/bash

set -e

echo "Building Docker images with Docker Compose..."
docker compose build

echo "Starting the application..."
docker compose up
