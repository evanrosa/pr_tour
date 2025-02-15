FROM apache/superset:latest

# Switch to root to install packages
USER root

# Install psycopg2-binary (or psycopg2)
RUN pip install psycopg2-binary

# Switch back to the default superset user
USER superset
