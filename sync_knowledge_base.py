"""
Script to sync Bedrock Knowledge Base data source
"""
import boto3
from botocore.exceptions import ClientError
import time

KB_ID = "DU9AYF1KM2"
DATA_SOURCE_ID = "TIPZQEWW66"  # S3 data source ID from Stack 2

def sync_knowledge_base():
    """Sync the Knowledge Base data source"""
    try:
        session = boto3.Session(profile_name='default')
        bedrock = session.client('bedrock-agent', region_name='us-east-1')
        
        print(f"Syncing Knowledge Base: {KB_ID}")
        print(f"Data Source: {DATA_SOURCE_ID}")
        print()
        
        # Start sync
        response = bedrock.start_ingestion_job(
            knowledgeBaseId=KB_ID,
            dataSourceId=DATA_SOURCE_ID
        )
        
        job_id = response['ingestionJob']['ingestionJobId']
        print(f"Sync job started: {job_id}")
        print("Waiting for sync to complete...")
        print()
        
        # Poll for completion
        max_wait = 300  # 5 minutes
        wait_time = 0
        check_interval = 10  # Check every 10 seconds
        
        while wait_time < max_wait:
            time.sleep(check_interval)
            wait_time += check_interval
            
            try:
                job_response = bedrock.get_ingestion_job(
                    knowledgeBaseId=KB_ID,
                    dataSourceId=DATA_SOURCE_ID,
                    ingestionJobId=job_id
                )
                
                status = job_response['ingestionJob']['status']
                print(f"Status: {status} (waited {wait_time}s)")
                
                if status == 'COMPLETE':
                    print()
                    print("=" * 60)
                    print("Sync Complete!")
                    print("=" * 60)
                    print(f"Knowledge Base ID: {KB_ID}")
                    print("The Knowledge Base is now ready to use.")
                    return True
                elif status == 'FAILED':
                    print()
                    print("=" * 60)
                    print("Sync Failed!")
                    print("=" * 60)
                    error = job_response['ingestionJob'].get('failureReasons', [])
                    if error:
                        print(f"Error: {error}")
                    return False
                    
            except ClientError as e:
                print(f"Error checking status: {e}")
                continue
        
        print()
        print("=" * 60)
        print("Sync is taking longer than expected.")
        print("Please check the AWS Console for status.")
        print("=" * 60)
        return False
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        print(f"[ERROR] {error_code}: {error_msg}")
        print()
        print("Alternative: Sync via AWS Console:")
        print("1. Go to: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/knowledgebases")
        print(f"2. Select Knowledge Base: {KB_ID}")
        print("3. Go to Data Sources tab")
        print("4. Click 'Sync' button")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    sync_knowledge_base()

