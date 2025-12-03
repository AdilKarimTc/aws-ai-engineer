"""Query PostgreSQL extensions"""
import boto3
import json

# Database configuration
CLUSTER_ARN = "arn:aws:rds:us-east-1:401040007987:cluster:my-aurora-serverless"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:401040007987:secret:auroraserverlessdb-KQc4kG"
DATABASE_NAME = "myapp"

def query_extensions():
    """Query pg_extension table"""
    try:
        session = boto3.Session(profile_name='default')
        rds_data = session.client('rds-data', region_name='us-east-1')
        
        print("=" * 80)
        print("PostgreSQL Extensions Query")
        print("=" * 80)
        print()
        print("Query: SELECT * FROM pg_extension;")
        print()
        
        response = rds_data.execute_statement(
            resourceArn=CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=DATABASE_NAME,
            sql="SELECT * FROM pg_extension;"
        )
        
        records = response.get('records', [])
        column_metadata = response.get('columnMetadata', [])
        
        if records:
            # Column names for pg_extension table
            column_names = ['oid', 'extname', 'extowner', 'extnamespace', 'extrelocatable', 'extversion', 'extconfig', 'extcondition']
            
            # Print headers
            header_line = " | ".join(column_names)
            print(header_line)
            print("-" * len(header_line))
            
            # Print rows
            for record in records:
                values = []
                for i, field in enumerate(record):
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
            print(f"Total extensions found: {len(records)}")
            print("=" * 80)
        else:
            print("No extensions found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_extensions()

