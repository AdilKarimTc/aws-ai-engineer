# AWS Bedrock Knowledge Base with Aurora Serverless

This project sets up an AWS Bedrock Knowledge Base integrated with an Aurora Serverless PostgreSQL database. It also includes scripts for database setup and file upload to S3.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Deployment Steps](#deployment-steps)
5. [Using the Scripts](#using-the-scripts)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)

## Project Overview

This project consists of several components:

1. Terraform configuration for creating:
   - A VPC
   - An Aurora Serverless PostgreSQL cluster
   - A Bedrock Knowledge Base
   - Necessary IAM roles and policies

2. A Python script for setting up the Aurora database schema
3. A Python script for uploading files to an S3 bucket

The goal is to create a Bedrock Knowledge Base that can leverage data stored in an Aurora Serverless database, with the ability to easily upload supporting documents to S3.

## Prerequisites

Before you begin, ensure you have the following:

- AWS CLI installed and configured with appropriate credentials
- Terraform installed (version 0.12 or later)
- Python 3.6 or later
- pip (Python package manager)

## Project Structure

```
project-root/
│
├── main.tf
├── modules/
│   ├── aurora_serverless/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── bedrock_kb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── scripts/
│   ├── aurora_setup.py
│   └── upload_to_s3.py
│
├── spec-sheets/
│   └── (your specification sheet files)
│
└── README.md
```

## Deployment Steps

1. Clone this repository to your local machine.

2. Navigate to the project root directory.

3. Initialize Terraform:
   ```
   terraform init
   ```

4. Review and modify the Terraform variables in `main.tf` as needed, particularly:
   - AWS region
   - VPC CIDR block
   - Aurora Serverless configuration
   - Bedrock Knowledge Base name

5. Deploy the infrastructure:
   ```
   terraform apply
   ```
   Review the planned changes and type "yes" to confirm.

6. After the Terraform deployment is complete, note the outputs, particularly the Aurora cluster endpoint.

7. Set up your Python environment:
   ```
   pip install psycopg2-binary boto3
   ```

8. Run the Aurora setup script:
   ```
   export DB_HOST=<your-aurora-cluster-endpoint>
   python scripts/aurora_setup.py
   ```

9. If you want to upload files to S3, place your files in the `spec-sheets` folder and run:
   ```
   python scripts/upload_to_s3.py
   ```
   Make sure to update the S3 bucket name in the script before running.

## Using the Scripts

### Aurora Setup Script

The `aurora_setup.py` script does the following:
- Connects to your Aurora Serverless database
- Creates the necessary extensions, schema, and tables
- Sets up the `bedrock_user` role

To use it:
1. Ensure the `DB_HOST` environment variable is set to your Aurora cluster endpoint.
2. Run `python scripts/aurora_setup.py`.

### S3 Upload Script

The `upload_to_s3.py` script does the following:
- Uploads all files from the `spec-sheets` folder to a specified S3 bucket
- Maintains the folder structure in S3

To use it:
1. Update the `bucket_name` variable in the script with your S3 bucket name.
2. Optionally, update the `prefix` variable if you want to upload to a specific path in the bucket.
3. Run `python scripts/upload_to_s3.py`.

## Customization

- To modify the VPC configuration, edit the `vpc` module call in `main.tf`.
- To change Aurora Serverless settings, modify the `aurora_serverless` module in `modules/aurora_serverless/main.tf`.
- To adjust the Bedrock Knowledge Base configuration, edit the `bedrock_kb` module in `modules/bedrock_kb/main.tf`.
- For different database schema or table structures, modify the SQL commands in `scripts/aurora_setup.py`.

## Troubleshooting

- If you encounter permissions issues, ensure your AWS credentials have the necessary permissions for creating all the resources.
- For database connection issues, check that the security group allows incoming connections on port 5432 from your IP address.
- If S3 uploads fail, verify that your AWS credentials have permission to write to the specified bucket.
- For any Terraform errors, ensure you're using a compatible version and that all module sources are correctly specified.

For more detailed troubleshooting, refer to the error messages and logs provided by Terraform and the Python scripts.