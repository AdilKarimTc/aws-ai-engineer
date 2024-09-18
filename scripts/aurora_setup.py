import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = "my-aurora-serverless-secret"
    region_name = "us-west-2"  # Change this to your AWS region

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']

def run_sql_commands():
    # Database connection parameters
    secret = json.loads(get_secret())
    db_params = {
        'dbname': 'myapp',
        'user': 'dbadmin',
        'password': secret['password'],
        'host': secret['host'],
        'port': '5432'
    }

    # Connect to the database
    conn = psycopg2.connect(**db_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # SQL commands to run
    sql_commands = [
        "CREATE EXTENSION IF NOT EXISTS vector;",
        "CREATE SCHEMA IF NOT EXISTS bedrock_integration;",
        "DO $$ BEGIN CREATE ROLE bedrock_user LOGIN; EXCEPTION WHEN duplicate_object THEN RAISE NOTICE 'Role already exists'; END $$;",
        "GRANT ALL ON SCHEMA bedrock_integration to bedrock_user;",
        "SET SESSION AUTHORIZATION bedrock_user;",
        """
        CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
          id uuid PRIMARY KEY,
          embedding vector(1536),
          chunks text,
          metadata json
        );
        """,
        "CREATE INDEX IF NOT EXISTS bedrock_kb_embedding_idx ON bedrock_integration.bedrock_kb USING hnsw (embedding vector_cosine_ops);"
    ]

    # Execute each SQL command
    for command in sql_commands:
        try:
            cursor.execute(command)
            print(f"Successfully executed: {command}")
        except psycopg2.Error as e:
            print(f"Error executing command: {command}")
            print(e)

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_sql_commands()