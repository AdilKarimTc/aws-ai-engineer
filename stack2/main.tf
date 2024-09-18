provider "aws" {
  region = "us-west-2"  # Change this to your desired region
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb"  # Make sure this path is correct

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn        = module.aurora_serverless.database_arn
  aurora_db_name    = module.aurora_serverless.database_name
  aurora_endpoint   = module.aurora_serverless.cluster_endpoint
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "chunks"
  aurora_verctor_field = "embedding"
  aurora_username   = module.aurora_serverless.database_master_username
  aurora_secret_arn = module.aurora_serverless.database_secretsmanager_secret_arn
  s3_bucket_arn = module.s3_bucket.s3_bucket_arn
}