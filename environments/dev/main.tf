provider "aws" {
  region = "us-west-2"  # Change this to your desired region
}

module "aurora_serverless" {
  source = "../modules/database"

  cluster_identifier = "my-aurora-serverless"
  master_password    = "changeme123!"  # Change this to a secure password
  vpc_id             = "vpc-12345678"  # Replace with your VPC ID

  # Optionally override other defaults
  database_name    = "myapp"
  master_username  = "dbadmin"
  max_capacity     = 8
  min_capacity     = 1
  allowed_cidr_blocks = ["10.0.0.0/16"]  # Replace with your allowed CIDR blocks
}