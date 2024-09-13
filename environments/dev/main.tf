provider "aws" {
  region = "us-west-2"  # Change this to your desired region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = "aurora-serverless-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

module "aurora_serverless" {
  source = "../modules/database"

  cluster_identifier = "my-aurora-serverless"
  master_password    = "changeme123!"  # Change this to a secure password
  vpc_id             = "vpc-12345678"  # Replace with your VPC ID

  # Optionally override other defaults
  database_name    = "myapp"
  master_username  = "dbadmin"
  max_capacity     = 1
  min_capacity     = 0.5
  allowed_cidr_blocks = ["10.0.0.0/16"]  # Replace with your allowed CIDR blocks
}

resource "aws_secretsmanager_secret" "aurora_password" {
  name = "aurora-password-secret"
}

resource "aws_secretsmanager_secret_version" "aurora_password" {
  secret_id     = aws_secretsmanager_secret.aurora_password.id
  secret_string = module.aurora_serverless.master_password
}

module "bedrock_kb" {
  source = "./modules/bedrock_kb"  # Make sure this path is correct

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_db_name    = module.aurora_serverless.database_name
  aurora_endpoint   = module.aurora_serverless.cluster_endpoint
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_username   = module.aurora_serverless.master_username
  aurora_secret_arn = aws_secretsmanager_secret.aurora_password.arn
}