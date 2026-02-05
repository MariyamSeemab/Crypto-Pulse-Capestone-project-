#!/bin/bash

# AWS CryptoPulse Deployment Script
# This script deploys the CryptoPulse application to AWS

set -e

# Configuration
PROJECT_NAME="CryptoPulse"
ENVIRONMENT="dev"
REGION="us-east-1"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

echo "🚀 Starting AWS deployment for ${PROJECT_NAME}..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI configured successfully"

# Deploy CloudFormation stack
echo "📦 Deploying CloudFormation infrastructure..."
aws cloudformation deploy \
    --template-file aws-infrastructure.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        ProjectName=$PROJECT_NAME \
        Environment=$ENVIRONMENT \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ CloudFormation stack deployed successfully"
else
    echo "❌ CloudFormation deployment failed"
    exit 1
fi

# Get stack outputs
echo "📋 Retrieving stack outputs..."
SNS_TOPIC_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`SNSTopicArn`].OutputValue' \
    --output text)

S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text)

echo "📝 Stack outputs:"
echo "  SNS Topic ARN: $SNS_TOPIC_ARN"
echo "  S3 Bucket: $S3_BUCKET"

# Create .env file from template
echo "⚙️  Creating environment configuration..."
if [ ! -f .env ]; then
    cp .env.aws.example .env
    echo "📝 Created .env file from template. Please update it with your values:"
    echo "  - SECRET_KEY: Generate a secure secret key"
    echo "  - SNS_TOPIC_ARN: $SNS_TOPIC_ARN"
    echo "  - S3_BUCKET: $S3_BUCKET"
    echo "  - AWS credentials (if not using IAM roles)"
fi

# Create initial admin user (optional)
echo "👤 Would you like to create an initial admin user? (y/n)"
read -r create_admin

if [ "$create_admin" = "y" ] || [ "$create_admin" = "Y" ]; then
    echo "📝 Enter admin username:"
    read -r admin_username
    echo "📝 Enter admin password:"
    read -s admin_password
    
    # This would require the application to be running
    echo "ℹ️  Admin user creation will be available after the application starts."
    echo "   Username: $admin_username"
    echo "   You can create the admin user through the application interface."
fi

echo ""
echo "🎉 AWS infrastructure deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Update the .env file with your configuration"
echo "2. Install dependencies: pip install -r requirements_aws.txt"
echo "3. Run the application: python app_aws.py"
echo "4. Access the application at http://localhost:5000"
echo ""
echo "🔧 For production deployment:"
echo "1. Deploy to EC2, ECS, or Lambda"
echo "2. Configure a load balancer"
echo "3. Set up a custom domain with Route 53"
echo "4. Enable HTTPS with ACM"
echo ""
echo "📊 Monitor your resources:"
echo "- DynamoDB tables in the AWS Console"
echo "- SNS notifications"
echo "- S3 bucket for file storage"