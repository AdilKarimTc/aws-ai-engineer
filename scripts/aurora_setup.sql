-- Create vector extension for Aurora PostgreSQL
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schema for Bedrock integration
CREATE SCHEMA IF NOT EXISTS bedrock_integration;

-- Create bedrock_user role (ignore error if already exists)
DO $$ 
BEGIN 
    CREATE ROLE bedrock_user LOGIN; 
EXCEPTION WHEN duplicate_object THEN 
    RAISE NOTICE 'Role already exists'; 
END $$;

-- Grant permissions on schema
GRANT ALL ON SCHEMA bedrock_integration to bedrock_user;

-- Switch to bedrock_user
SET SESSION AUTHORIZATION bedrock_user;

-- Create the table for storing embeddings
CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
    id uuid PRIMARY KEY,
    embedding vector(1536),
    chunks text,
    metadata json
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS bedrock_kb_embedding_idx 
ON bedrock_integration.bedrock_kb 
USING hnsw (embedding vector_cosine_ops);

-- Create GIN index for full-text search on chunks column (required by Bedrock)
CREATE INDEX IF NOT EXISTS bedrock_kb_chunks_idx 
ON bedrock_integration.bedrock_kb 
USING gin (to_tsvector('english', chunks));