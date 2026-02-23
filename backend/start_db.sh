#!/bin/bash

# Run PostgreSQL in a Docker container
docker run --name forethemoney-db \
  -e POSTGRES_USER=forethemoney \
  -e POSTGRES_PASSWORD=forethemoney123 \
  -e POSTGRES_DB=forethemoney \
  -p 5433:5433 \
  -d postgres:15

docker ps
echo "PostgreSQL database started in Docker container 'forethemoney-db'."