# CryptoPulse AWS Edition

A comprehensive cryptocurrency tracking and portfolio management application built with Flask and AWS services.

## 🏗️ Architecture

This AWS version of CryptoPulse leverages multiple AWS services for scalability and reliability:

- **DynamoDB**: User data, portfolios, transactions, and price alerts
- **SNS**: Real-time notifications for trades and alerts
- **S3**: File storage for future features
- **IAM**: Secure access management
- **CloudFormation**: Infrastructure as Code

## 🚀 Features

### Core Features
- **Multi-Currency Support**: Track prices in 10 major world currencies
- **Real-Time Price Tracking**: Live cryptocurrency prices via CoinGecko API
- **Virtual Trading**: Buy and sell cryptocurrencies with virtual money
- **Portfolio Management**: Track holdings, profits, and losses
- **Interactive Charts**: Historical price charts with Chart.js
- **Admin Dashboard**: System statistics and user management
- **Dual Login System**: Separate interfaces for users and administrators

### AWS-Specific Features
- **Scalable Database**: DynamoDB for high-performance data storage
- **Real-Time Notifications**: SNS integration for trade alerts
- **Cloud Storage**: S3 integration for file uploads
- **Infrastructure as Code**: CloudFormation templates
- **Production Ready**: Designed for AWS deployment

## 📋 Prerequisites

- Python 3.8+
- AWS Account with appropriate permissions
- AWS CLI configured
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cryptopulse-aws
```

### 2. Install Dependencies
```bash
pip install -r requirements_aws.txt
```

### 3. Deploy AWS Infrastructure
```bash
# Make the deployment script executable
chmod +x deploy-aws.sh

# Run the deployment
./deploy-aws.sh
```

### 4. Configure Environment
```bash
# Copy the environment template
cp .env.aws.example .env

# Edit the .env file with your AWS configuration
nano .env
```

Required environment variables:
```env
SECRET_KEY=your_super_secret_key_here
AWS_REGION=us-east-1
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications
S3_BUCKET=cryptopulse-files-bucket
```

### 5. Run the Application
```bash
python app_aws.py
```

The application will be available at `http://localhost:5000`

## 🗄️ Database Schema

### DynamoDB Tables

#### Users Table
```
Primary Key: username (String)
Attributes:
- password (String, hashed)
- email (String)
- role (String: 'user' | 'admin')
- created_at (String, ISO timestamp)
```

#### Portfolios Table
```
Primary Key: username (String)
Attributes:
- balance (Number, Decimal)
- holdings (Map: coin_id -> quantity)
- created_at (String, ISO timestamp)
```

#### Transactions Table
```
Primary Key: username (String)
Sort Key: timestamp (String)
Attributes:
- transaction_id (String, UUID)
- type (String: 'buy' | 'sell')
- coin_id (String)
- quantity (Number, Decimal)
- price (Number, Decimal)
- amount (Number, Decimal)
```

#### Price Alerts Table
```
Primary Key: username (String)
Sort Key: alert_id (String)
Attributes:
- coin_id (String)
- target_price (Number, Decimal)
- condition (String: 'above' | 'below')
- active (Boolean)
- created_at (String, ISO timestamp)
```

## 🔧 Configuration

### AWS Permissions

The application requires the following AWS permissions:

#### DynamoDB
- `dynamodb:GetItem`
- `dynamodb:PutItem`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`
- `dynamodb:Query`
- `dynamodb:Scan`

#### SNS
- `sns:Publish`

#### S3
- `s3:GetObject`
- `s3:PutObject`
- `s3:DeleteObject`
- `s3:ListBucket`

### Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Cardano (ADA)
- Polkadot (DOT)
- Chainlink (LINK)
- Litecoin (LTC)
- Bitcoin Cash (BCH)
- Stellar (XLM)
- Dogecoin (DOGE)
- Ripple (XRP)
- Avalanche (AVAX)
- Polygon (MATIC)
- Uniswap (UNI)
- Cosmos (ATOM)
- Algorand (ALGO)
- Tezos (XTZ)
- Filecoin (FIL)
- Internet Computer (ICP)
- VeChain (VET)
- Theta (THETA)
- Elrond (EGLD)

### Supported Currencies
- USD (US Dollar) - $
- EUR (Euro) - €
- GBP (British Pound) - £
- JPY (Japanese Yen) - ¥
- CAD (Canadian Dollar) - C$
- AUD (Australian Dollar) - A$
- CHF (Swiss Franc) - CHF
- CNY (Chinese Yuan) - ¥
- INR (Indian Rupee) - ₹
- KRW (South Korean Won) - ₩

## 🚀 Deployment

### Local Development
```bash
python app_aws.py
```

### AWS EC2 Deployment
1. Launch an EC2 instance with the application IAM role
2. Install dependencies and copy application files
3. Configure environment variables
4. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_aws:app
```

### AWS Lambda Deployment
1. Package the application with dependencies
2. Create a Lambda function with the application IAM role
3. Configure API Gateway for HTTP routing
4. Set environment variables in Lambda configuration

### AWS ECS Deployment
1. Create a Docker image with the application
2. Push to Amazon ECR
3. Create an ECS service with the application IAM role
4. Configure Application Load Balancer

## 📊 Monitoring

### CloudWatch Metrics
- DynamoDB read/write capacity
- Lambda function duration and errors
- SNS message delivery status
- Application logs

### SNS Notifications
The application sends notifications for:
- User registration and login
- Cryptocurrency purchases and sales
- Admin actions
- System alerts

## 🔐 Security

### Best Practices Implemented
- Password hashing with Werkzeug
- Session management with Flask
- AWS IAM role-based access
- Environment variable configuration
- Input validation and sanitization
- HTTPS ready (configure with ALB/CloudFront)

### Production Security Checklist
- [ ] Use strong SECRET_KEY
- [ ] Enable DynamoDB encryption at rest
- [ ] Configure VPC for network isolation
- [ ] Set up AWS WAF for web application firewall
- [ ] Enable CloudTrail for audit logging
- [ ] Use AWS Secrets Manager for sensitive data
- [ ] Configure HTTPS with ACM certificates

## 🧪 Testing

### Local Testing
```bash
# Test DynamoDB connection
python -c "import boto3; print(boto3.resource('dynamodb').tables.all())"

# Test SNS notifications
python -c "import boto3; boto3.client('sns').publish(TopicArn='your-topic-arn', Message='Test')"
```

### Load Testing
Use AWS Load Testing solution or tools like Apache Bench:
```bash
ab -n 1000 -c 10 http://your-app-url/
```

## 🐛 Troubleshooting

### Common Issues

#### DynamoDB Access Denied
- Check IAM permissions
- Verify table names match configuration
- Ensure region is correct

#### SNS Publish Errors
- Verify SNS topic ARN
- Check IAM permissions for SNS
- Confirm topic exists in the correct region

#### Application Won't Start
- Check environment variables
- Verify AWS credentials
- Review CloudWatch logs

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Scaling

### Performance Optimization
- Use DynamoDB auto-scaling
- Implement caching with ElastiCache
- Use CloudFront for static assets
- Configure read replicas for heavy read workloads

### Cost Optimization
- Use DynamoDB on-demand billing for variable workloads
- Implement S3 lifecycle policies
- Use Reserved Instances for predictable workloads
- Monitor costs with AWS Cost Explorer

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check AWS documentation for service-specific issues
- Review CloudWatch logs for application errors

## 🔄 Updates

### Version History
- v1.0.0: Initial AWS implementation
- Features: DynamoDB integration, SNS notifications, CloudFormation templates

### Roadmap
- [ ] Price alerts with SNS
- [ ] Advanced charting features
- [ ] Mobile responsive improvements
- [ ] API rate limiting
- [ ] Automated backups
- [ ] Multi-region deployment