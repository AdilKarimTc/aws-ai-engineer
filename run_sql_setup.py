"""
Script to run SQL setup on Aurora database using RDS Data API
"""
import boto3
from botocore.exceptions import ClientError
import json

# Database configuration
CLUSTER_ARN = "arn:aws:rds:us-east-1:401040007987:cluster:my-aurora-serverless"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:401040007987:secret:auroraserverlessdb-KQc4kG"
DATABASE_NAME = "myapp"

# SQL statements to execute
SQL_STATEMENTS = [
    "CREATE EXTENSION IF NOT EXISTS vector;",
    "CREATE SCHEMA IF NOT EXISTS bedrock_integration;",
    """DO $$ 
BEGIN 
    CREATE ROLE bedrock_user LOGIN; 
EXCEPTION WHEN duplicate_object THEN 
    RAISE NOTICE 'Role already exists'; 
END $$;""",
    "GRANT ALL ON SCHEMA bedrock_integration to bedrock_user;",
    "SET SESSION AUTHORIZATION bedrock_user;",
    """CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
    id uuid PRIMARY KEY,
    embedding vector(1536),
    chunks text,
    metadata json
);""",
    """CREATE INDEX IF NOT EXISTS bedrock_kb_embedding_idx 
ON bedrock_integration.bedrock_kb 
USING hnsw (embedding vector_cosine_ops);""",
    """CREATE INDEX IF NOT EXISTS bedrock_kb_chunks_idx 
ON bedrock_integration.bedrock_kb 
USING gin (to_tsvector('english', chunks));"""
]

def run_sql_statement(rds_data, sql, database=DATABASE_NAME):
    """Execute a single SQL statement"""
    try:
        response = rds_data.execute_statement(
            resourceArn=CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=database,
            sql=sql
        )
        return response
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        
        # Some errors are expected (like duplicate_object)
        if 'duplicate_object' in error_msg.lower() or 'already exists' in error_msg.lower():
            print(f"   [INFO] {error_msg[:100]}")
            return None
        else:
            raise

def main():
    print("=" * 60)
    print("Aurora Database SQL Setup")
    print("=" * 60)
    print()
    print(f"Cluster ARN: {CLUSTER_ARN}")
    print(f"Database: {DATABASE_NAME}")
    print()
    
    try:
        # Initialize RDS Data API client
        session = boto3.Session(profile_name='default')
        rds_data = session.client('rds-data', region_name='us-east-1')
        
        print("Executing SQL statements...")
        print()
        
        for i, sql in enumerate(SQL_STATEMENTS, 1):
            print(f"[{i}/{len(SQL_STATEMENTS)}] Executing statement...")
            try:
                response = run_sql_statement(rds_data, sql)
                if response:
                    print(f"   [OK] Statement executed successfully")
                else:
                    print(f"   [OK] Statement completed (expected message)")
            except ClientError as e:
                error_msg = e.response.get('Error', {}).get('Message', str(e))
                print(f"   [ERROR] {error_msg}")
                # Continue with next statement
                continue
            except Exception as e:
                print(f"   [ERROR] Unexpected error: {e}")
                continue
        
        print()
        print("=" * 60)
        print("SQL Setup Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Verify the table exists (optional)")
        print("2. Deploy Stack 2: cd stack2 && terraform apply")
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        
        if error_code == 'BadRequestException':
            print(f"[ERROR] Bad Request: {error_msg}")
            print()
            print("This might mean:")
            print("- RDS Data API is not enabled for this cluster")
            print("- The database name might be incorrect")
            print()
            print("Alternative: Use AWS RDS Query Editor:")
            print("1. Go to: https://console.aws.amazon.com/rds/home?region=us-east-1#query-editor:")
            print("2. Connect to: my-aurora-serverless")
            print("3. Use Secret ARN: arn:aws:secretsmanager:us-east-1:401040007987:secret:auroraserverlessdb-KQc4kG")
            print("4. Copy and paste SQL from scripts/aurora_setup.sql")
        else:
            print(f"[ERROR] {error_code}: {error_msg}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    main()

