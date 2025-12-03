"""
Verification script to check project setup status
"""
import boto3
from botocore.exceptions import ClientError, ProfileNotFound
import json
import os

# Force use of default profile
os.environ.pop('AWS_PROFILE', None)

def check_aws_credentials():
    """Verify AWS credentials are configured"""
    try:
        # Explicitly use default profile
        session = boto3.Session(profile_name='default')
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"[OK] AWS Credentials: Valid")
        print(f"   Account: {identity.get('Account')}")
        print(f"   User: {identity.get('Arn')}")
        return True
    except ProfileNotFound as e:
        print(f"[ERROR] AWS Profile not found: {e}")
        print(f"   Try running: ./configure_aws.bat")
        return False
    except Exception as e:
        error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"[ERROR] AWS Credentials: Invalid - {error_msg}")
        return False

def check_s3_bucket(bucket_name):
    """Check if S3 bucket exists and is accessible"""
    try:
        session = boto3.Session(profile_name='default')
        s3 = session.client('s3')
        s3.head_bucket(Bucket=bucket_name)
        print(f"[OK] S3 Bucket: {bucket_name} exists")
        
        # List objects
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='spec-sheets/', MaxKeys=5)
        if 'Contents' in response:
            print(f"   Found {len(response['Contents'])} files in spec-sheets/")
            for obj in response['Contents'][:3]:
                print(f"   - {obj['Key']}")
        else:
            print(f"   [WARNING] No files found in spec-sheets/ folder")
        return True
    except ClientError as e:
        print(f"[ERROR] S3 Bucket: {bucket_name} - {e}")
        return False

def check_rds_cluster(cluster_identifier):
    """Check if RDS cluster exists"""
    try:
        session = boto3.Session(profile_name='default')
        rds = session.client('rds')
        response = rds.describe_db_clusters(DBClusterIdentifier=cluster_identifier)
        cluster = response['DBClusters'][0]
        status = cluster['Status']
        endpoint = cluster.get('Endpoint', 'N/A')
        print(f"[OK] RDS Cluster: {cluster_identifier}")
        print(f"   Status: {status}")
        print(f"   Endpoint: {endpoint}")
        return True
    except ClientError as e:
        print(f"[ERROR] RDS Cluster: {cluster_identifier} - {e}")
        return False

def check_bedrock_kb(kb_id=None):
    """Check if Bedrock Knowledge Base exists"""
    try:
        session = boto3.Session(profile_name='default')
        bedrock = session.client('bedrock-agent', region_name='us-east-1')
        if kb_id:
            response = bedrock.get_knowledge_base(knowledgeBaseId=kb_id)
            kb = response['knowledgeBase']
            print(f"[OK] Bedrock Knowledge Base: {kb_id}")
            print(f"   Name: {kb.get('name', 'N/A')}")
            print(f"   Status: {kb.get('status', 'N/A')}")
            return True
        else:
            # List all knowledge bases
            response = bedrock.list_knowledge_bases()
            kbs = response.get('knowledgeBaseSummaries', [])
            if kbs:
                print(f"[OK] Found {len(kbs)} Knowledge Base(s):")
                for kb in kbs:
                    print(f"   - {kb['name']} (ID: {kb['knowledgeBaseId']})")
                return True
            else:
                print(f"[WARNING] No Knowledge Bases found")
                return False
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        if error_code == 'ResourceNotFoundException':
            print(f"[WARNING] Bedrock Knowledge Base: Not found (Stack 2 may not be deployed)")
        else:
            print(f"[ERROR] Bedrock Knowledge Base: {e}")
        return False

def main():
    print("=" * 60)
    print("Project Setup Verification")
    print("=" * 60)
    print()
    
    # Check AWS credentials
    if not check_aws_credentials():
        print("\n[WARNING] Please configure AWS credentials first using configure_aws.bat")
        return
    
    print()
    
    # Check S3 bucket
    check_s3_bucket("bedrock-kb-401040007987")
    print()
    
    # Check RDS cluster
    check_rds_cluster("my-aurora-serverless")
    print()
    
    # Check Bedrock Knowledge Base
    check_bedrock_kb()
    print()
    
    print("=" * 60)
    print("Verification Complete")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. If RDS is OK but KB not found: Run SQL script, then deploy Stack 2")
    print("2. If S3 has no files: Run python scripts/upload_s3.py")
    print("3. If KB exists: Get KB ID and update app.py")

if __name__ == "__main__":
    main()

