resource "aws_bedrock_knowledge_base" "main" {
  knowledge_base_name = var.knowledge_base_name
  description         = var.knowledge_base_description
  storage_configuration {
    type = "VECTOR"
  }
}

resource "aws_bedrock_data_source" "aurora" {
  name              = "aurora-data-source"
  knowledge_base_id = aws_bedrock_knowledge_base.main.id
  data_source_configuration {
    type = "AMAZON_AURORA"
    amazon_aurora {
      database_name = var.aurora_db_name
      hostname      = var.aurora_endpoint
      port          = 5432
      table_name    = var.aurora_table_name
      username      = var.aurora_username
      secret_arn    = var.aurora_secret_arn
    }
  }
}

resource "aws_iam_role" "bedrock_kb_role" {
  name = "${var.knowledge_base_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_kb_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBedrockKnowledgeBaseServiceRolePolicy"
  role       = aws_iam_role.bedrock_kb_role.name
}