provider "aws" {
  region = "us-east-1"  # Using us-east-1 for Udacity Cloud Lab
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb" 

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn        = "arn:aws:rds:us-east-1:401040007987:cluster:my-aurora-serverless"
  aurora_db_name    = "myapp"
  aurora_endpoint   = "my-aurora-serverless.cluster-cic79iy4objl.us-east-1.rds.amazonaws.com"
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "chunks"
  aurora_verctor_field = "embedding"
  aurora_username   = "dbadmin"
  aurora_secret_arn = "arn:aws:secretsmanager:us-east-1:401040007987:secret:auroraserverlessdb-KQc4kG"
  s3_bucket_arn = "arn:aws:s3:::bedrock-kb-401040007987"
}