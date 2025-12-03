# 🚀 Quick Start Guide

Follow these steps in order to deploy your AWS Bedrock Knowledge Base project.

## ✅ Step 1: Configure AWS Credentials

Run the configuration script:
```cmd
configure_aws.bat
```

This will automatically set up your AWS credentials and verify connectivity.

**Expected Output**: You should see your AWS Account ID and User ARN displayed.

---

## ✅ Step 2: Setup Python Environment

Run the setup script:
```cmd
setup_phase1.bat
```

This will:
- Create a Python virtual environment
- Install all required dependencies (boto3, streamlit)

---

## ✅ Step 3: Deploy Infrastructure Stack 1

**What it creates**: VPC, Aurora PostgreSQL Database, S3 Bucket

```cmd
cd stack1
terraform init
terraform apply
```

⏱️ **Wait Time**: 15-20 minutes

📝 **IMPORTANT**: Save these outputs to `outputs_template.txt`:
- `aurora_cluster_endpoint`
- `aurora_cluster_arn`
- `db_secret_arn`
- `s3_bucket_name`

---

## ✅ Step 4: Setup Database

1. Go to AWS Console → **RDS** → **Query Editor**
2. Connect using:
   - Database: Select your Aurora cluster
   - Auth: Secrets Manager ARN (use the `db_secret_arn` from Step 3)
   - Database name: `myapp`
3. Copy content from `scripts/aurora_sql.sql`
4. Paste and click **Run**

✓ **Success**: "Query successfully executed"

---

## ✅ Step 5: Update Stack 2 Configuration

Open `stack2/main.tf` and update:

```terraform
aurora_arn        = "YOUR_AURORA_CLUSTER_ARN"
aurora_endpoint   = "YOUR_AURORA_ENDPOINT"
aurora_secret_arn = "YOUR_DB_SECRET_ARN"
s3_bucket_arn     = "arn:aws:s3:::YOUR_S3_BUCKET_NAME"
```

---

## ✅ Step 6: Deploy Infrastructure Stack 2

**What it creates**: Bedrock Knowledge Base

```cmd
cd ..\stack2
terraform init
terraform apply
```

📝 **IMPORTANT**: Save the `knowledge_base_id` output

---

## ✅ Step 7: Upload Documents

1. Update `scripts/upload_s3.py` line 35 with your S3 bucket name
2. Run:
```cmd
cd ..
python scripts\upload_s3.py
```

3. Sync Knowledge Base:
   - AWS Console → **Bedrock** → **Knowledge Bases**
   - Select your KB → **Data Sources** → Click **Sync**
   - Wait for "Available" status

---

## ✅ Step 8: Run the Application

1. Update `app.py` line 14 with your Knowledge Base ID
2. Run:
```cmd
streamlit run app.py
```

3. Test with: *"What are the specifications for the excavator X950?"*

---

## 🎯 You're Done!

Your chatbot should now respond to queries about heavy machinery using the uploaded PDF documentation.

## 📚 Need More Details?

See `DEPLOYMENT_GUIDE.md` for detailed explanations and troubleshooting.
