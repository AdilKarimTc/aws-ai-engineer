output "db_endpoint" {
  value = module.aurora_serverless.cluster_endpoint
}

output "db_reader_endpoint" {
  value = module.aurora_serverless.cluster_reader_endpoint
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnets
}

output "public_subnet_ids" {
  value = module.vpc.public_subnets
}

output "bedrock_knowledge_base_id" {
  value = module.bedrock_kb.id
}

output "bedrock_knowledge_base_arn" {
  value = module.bedrock_kb.arn
}

output "aurora_endpoint" {
  value = module.aurora_serverless.cluster_endpoint
}