#!/bin/bash
set -e

# Load config from .env
if [ -f .env ]; then
  export $(cat .env | xargs)
else
  echo "❌ .env file not found. Please create one."
  exit 1
fi

# === FUNCTIONS ===

create_network() {
  echo "🔗 Creating network: $NETWORK"
  docker network create $NETWORK || true
}

start_db() {
  echo "🚀 Starting Postgres container..."
  docker run -d \
    --name $DB_CONTAINER \
    --network $NETWORK \
    -e POSTGRES_DB=$DB_NAME \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_PASSWORD=$DB_PASS \
    -p 5432:5432 \
    $DB_IMAGE
}

wait_for_db() {
  echo "⏳ Waiting for Postgres to be ready..."
  until docker exec $DB_CONTAINER pg_isready -U $DB_USER > /dev/null 2>&1; do
    sleep 2
  done
  echo "✅ Postgres is ready."
}

build_etl_image() {
  echo "🔨 Building ETL image..."
  docker build -t $ETL_IMAGE .
}

run_stage() {
  stage=$1
  script=$2
  echo "▶️ Running $stage..."
  docker run --rm \
    --network $NETWORK \
    -v $(pwd):/app \
    $ETL_IMAGE python $script
}

show_results() {
  echo "📊 Showing data from database..."
  docker exec -it $DB_CONTAINER \
    psql -U $DB_USER -d $DB_NAME -c "TABLE matches;"
}

cleanup() {
  echo "🧹 Cleaning up containers and network..."
  docker stop $DB_CONTAINER || true
  docker rm $DB_CONTAINER || true
  docker network rm $NETWORK || true
  echo "✅ Cleanup done."
}

# === MAIN PIPELINE ===
create_network
start_db
wait_for_db
build_etl_image

run_stage "Extract" scraper.py
run_stage "Transform" transform.py
run_stage "Load" load.py

show_results
cleanup