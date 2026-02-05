#!/usr/bin/env python3
"""
Initialize Admin User for CryptoPulse AWS
This script creates the first admin user in DynamoDB
"""

import boto3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime
from botocore.exceptions import ClientError

def create_admin_user():
    """Create initial admin user in DynamoDB"""
    
    # AWS Configuration
    region = os.environ.get('AWS_REGION', 'us-east-1')
    table_name = os.environ.get('USERS_TABLE', 'CryptoPulse_Users')
    
    try:
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name=region)
        users_table = dynamodb.Table(table_name)
        
        print("🔧 CryptoPulse AWS Admin Initialization")
        print("=" * 50)
        
        # Get admin credentials
        admin_username = input("Enter admin username: ").strip()
        if not admin_username:
            print("❌ Username cannot be empty")
            return False
            
        admin_password = input("Enter admin password: ").strip()
        if not admin_password:
            print("❌ Password cannot be empty")
            return False
            
        admin_email = input("Enter admin email (optional): ").strip()
        
        # Check if admin already exists
        try:
            response = users_table.get_item(Key={'username': admin_username})
            if 'Item' in response:
                print(f"❌ User '{admin_username}' already exists")
                return False
        except ClientError as e:
            print(f"❌ Error checking existing user: {e}")
            return False
        
        # Create admin user
        hashed_password = generate_password_hash(admin_password)
        
        admin_user = {
            'username': admin_username,
            'password': hashed_password,
            'email': admin_email,
            'role': 'admin',
            'created_at': datetime.now().isoformat()
        }
        
        users_table.put_item(Item=admin_user)
        
        print(f"✅ Admin user '{admin_username}' created successfully!")
        print(f"📧 Email: {admin_email if admin_email else 'Not provided'}")
        print(f"🔑 Role: admin")
        print(f"📅 Created: {admin_user['created_at']}")
        
        return True
        
    except ClientError as e:
        print(f"❌ AWS Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_aws_setup():
    """Verify AWS configuration and connectivity"""
    
    print("🔍 Verifying AWS setup...")
    
    try:
        # Check AWS credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS Account: {identity.get('Account')}")
        print(f"✅ User/Role: {identity.get('Arn')}")
        
        # Check DynamoDB access
        region = os.environ.get('AWS_REGION', 'us-east-1')
        table_name = os.environ.get('USERS_TABLE', 'CryptoPulse_Users')
        
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        
        # Try to describe the table
        table.load()
        print(f"✅ DynamoDB table '{table_name}' accessible")
        print(f"✅ Table status: {table.table_status}")
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"❌ DynamoDB table '{table_name}' not found")
            print("💡 Run the CloudFormation deployment first: ./deploy-aws.sh")
        elif error_code == 'AccessDeniedException':
            print("❌ Access denied to DynamoDB")
            print("💡 Check your AWS credentials and IAM permissions")
        else:
            print(f"❌ AWS Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    
    print("🚀 CryptoPulse AWS Admin Initialization")
    print("=" * 50)
    
    # Verify AWS setup first
    if not verify_aws_setup():
        print("\n❌ AWS setup verification failed")
        print("Please ensure:")
        print("1. AWS credentials are configured (aws configure)")
        print("2. CloudFormation stack is deployed (./deploy-aws.sh)")
        print("3. IAM permissions are correct")
        return
    
    print("\n" + "=" * 50)
    
    # Create admin user
    if create_admin_user():
        print("\n🎉 Admin user initialization completed!")
        print("\nNext steps:")
        print("1. Start the application: python app_aws.py")
        print("2. Access admin dashboard at: http://localhost:5000")
        print("3. Login with admin credentials")
    else:
        print("\n❌ Admin user initialization failed")

if __name__ == '__main__':
    main()