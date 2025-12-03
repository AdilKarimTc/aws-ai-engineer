"""Query bedrock_integration.bedrock_kb table information"""
import boto3
import json

# Database configuration
CLUSTER_ARN = "arn:aws:rds:us-east-1:401040007987:cluster:my-aurora-serverless"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:401040007987:secret:auroraserverlessdb-KQc4kG"
DATABASE_NAME = "myapp"

def query_bedrock_table():
    """Query information_schema to show bedrock_integration.bedrock_kb table"""
    try:
        session = boto3.Session(profile_name='default')
        rds_data = session.client('rds-data', region_name='us-east-1')
        
        print("=" * 80)
        print("Bedrock Integration Table Query")
        print("=" * 80)
        print()
        
        query = """SELECT
        table_schema || '.' || table_name as show_tables
FROM
        information_schema.tables
WHERE
        table_type = 'BASE TABLE'
AND
        table_schema = 'bedrock_integration';"""
        
        print("Query:")
        print(query)
        print()
        
        response = rds_data.execute_statement(
            resourceArn=CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=DATABASE_NAME,
            sql=query
        )
        
        records = response.get('records', [])
        column_metadata = response.get('columnMetadata', [])
        
        if records:
            # Print headers
            print("show_tables")
            print("-" * 80)
            
            # Print rows
            for record in records:
                values = []
                for field in record:
                    if 'stringValue' in field:
                        values.append(field['stringValue'])
                    elif 'longValue' in field:
                        values.append(str(field['longValue']))
                    elif 'doubleValue' in field:
                        values.append(str(field['doubleValue']))
                    elif 'booleanValue' in field:
                        values.append(str(field['booleanValue']))
                    elif 'isNull' in field and field['isNull']:
                        values.append('NULL')
                    else:
                        values.append('')
                print(" | ".join(values))
            
            print()
            print("=" * 80)
            print(f"Total tables found: {len(records)}")
            print("=" * 80)
        else:
            print("No tables found in bedrock_integration schema")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_bedrock_table()

