#!/bin/bash
set -e
export PGPASSWORD="${POSTGRES_PASSWORD}"
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "postgres" <<-EOSQL
    CREATE DATABASE pr_tour_superset;
    -- Optionally, create other databases here
    GRANT ALL PRIVILEGES ON DATABASE pr_tour_superset TO ${POSTGRES_USER};
EOSQL