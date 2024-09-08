output "cluster_endpoint" {
  description = "The cluster endpoint"
  value       = aws_rds_cluster.aurora_serverless.endpoint
}

output "cluster_reader_endpoint" {
  description = "The cluster reader endpoint"
  value       = aws_rds_cluster.aurora_serverless.reader_endpoint
}

output "cluster_id" {
  description = "The cluster identifier"
  value       = aws_rds_cluster.aurora_serverless.id
}