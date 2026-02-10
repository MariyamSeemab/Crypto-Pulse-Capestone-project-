# AWS SNS Email Notifications Setup Guide

## 📧 Overview

CryptoPulse now supports email notifications via AWS SNS (Simple Notification Service) for all buy/sell transactions. Users receive professional email confirmations whenever they trade cryptocurrency.

---

## 🚀 Quick Start

### Option 1: Run Without AWS (Mock Mode)
The application works without AWS configuration. Notifications will be logged to console instead of sent via email.

```bash
python app.py
```

### Option 2: Run With AWS SNS
Configure AWS credentials and SNS topic to enable real email notifications.

---

## 🔧 AWS SNS Configuration

### Step 1: Install boto3
```bash
pip install boto3
```

Or update requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Create SNS Topic

1. **Login to AWS Console**: https://console.aws.amazon.com/sns/
2. **Navigate to SNS**: Services → Simple Notification Service
3. **Create Topic**:
   - Click "Create topic"
   - Type: Standard
   - Name: `cryptopulse-notifications`
   - Display name: `CryptoPulse Alerts`
   - Click "Create topic"

4. **Copy Topic ARN**: 
   - Example: `arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications`

### Step 3: Create Email Subscription

1. **In your SNS topic**, click "Create subscription"
2. **Protocol**: Email
3. **Endpoint**: Your email address (e.g., `your-email@example.com`)
4. **Click "Create subscription"**
5. **Confirm subscription**: Check your email and click the confirmation link

### Step 4: Configure AWS Credentials

#### Method A: Environment Variables (Recommended)
```bash
# Windows (CMD)
set AWS_REGION=us-east-1
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications

# Windows (PowerShell)
$env:AWS_REGION="us-east-1"
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:SNS_TOPIC_ARN="arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications"

# Linux/Mac
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications
```

#### Method B: AWS CLI Configuration
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter default region: us-east-1
# Enter default output format: json
```

Then set SNS_TOPIC_ARN:
```bash
set SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications
```

#### Method C: .env File
Create a `.env` file in the project root:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Add to app.py (at the top):
```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 5: Set IAM Permissions

Your AWS user/role needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "sns:Subscribe",
                "sns:ListTopics"
            ],
            "Resource": "arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications"
        }
    ]
}
```

---

## 📧 Email Notification Features

### What Gets Sent

**Buy Transaction Email:**
```
Subject: 🛒 CryptoPulse - Purchase Confirmation: BITCOIN

Transaction Type:  BUY
Cryptocurrency:    BITCOIN
Quantity:          0.00123456 BTC
Price per Unit:    $45,000.00
Total Amount:      $55.56
Transaction Time:  2026-02-10 14:30:45 UTC
```

**Sell Transaction Email:**
```
Subject: 💰 CryptoPulse - Sale Confirmation: ETHEREUM

Transaction Type:  SELL
Cryptocurrency:    ETHEREUM
Quantity:          0.50000000 ETH
Price per Unit:    $3,000.00
Total Amount:      $1,500.00
Transaction Time:  2026-02-10 14:35:22 UTC
```

### Email Content Includes:
- ✅ Transaction type (Buy/Sell)
- ✅ Cryptocurrency name
- ✅ Quantity traded
- ✅ Price per unit
- ✅ Total amount
- ✅ Timestamp
- ✅ Quick links to portfolio, charts, and news
- ✅ Professional formatting
- ✅ Important disclaimers

---

## 🧪 Testing

### Test Without AWS (Mock Mode)
```bash
python app.py
```

Console output will show:
```
⚠️ AWS SNS disabled: SNS_TOPIC_ARN not configured
📧 [MOCK] Email would be sent: 🛒 CryptoPulse - Purchase Confirmation: BITCOIN
   To: demo@user.com
   Message: Transaction Type: BUY...
```

### Test With AWS SNS
1. Configure AWS credentials (see Step 4)
2. Start application:
```bash
python app.py
```

Console output will show:
```
✅ AWS SNS initialized for region: us-east-1
```

3. Login and make a trade
4. Check console for:
```
✅ SNS notification sent to demo@user.com: abc123-message-id
```

5. Check your email inbox for the notification

---

## 🔍 Troubleshooting

### Issue: "boto3 not installed"
**Solution:**
```bash
pip install boto3
```

### Issue: "SNS_TOPIC_ARN not configured"
**Solution:** Set the environment variable:
```bash
set SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications
```

### Issue: "Access Denied" when sending SNS
**Solution:** Check IAM permissions. User needs `sns:Publish` permission.

### Issue: Email not received
**Checklist:**
- ✅ SNS subscription confirmed (check email for confirmation link)
- ✅ Check spam/junk folder
- ✅ Verify email address in SNS subscription
- ✅ Check AWS CloudWatch logs for errors

### Issue: "ClientError: InvalidParameter"
**Solution:** Verify SNS_TOPIC_ARN format:
```
arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME
```

---

## 💰 AWS Costs

### SNS Pricing (as of 2026)
- **First 1,000 email notifications**: FREE
- **Additional emails**: $2.00 per 100,000 notifications
- **SMS**: Additional charges apply

### Estimated Costs for CryptoPulse
- **Low usage** (100 trades/month): FREE
- **Medium usage** (10,000 trades/month): FREE
- **High usage** (100,000 trades/month): ~$2.00/month

**Note:** Always check current AWS pricing at https://aws.amazon.com/sns/pricing/

---

## 🔐 Security Best Practices

### 1. Never Commit Credentials
Add to `.gitignore`:
```
.env
*.pem
*.key
aws_credentials.txt
```

### 2. Use IAM Roles (Production)
For EC2/Lambda deployment, use IAM roles instead of access keys.

### 3. Rotate Access Keys
Rotate AWS access keys every 90 days.

### 4. Use Least Privilege
Grant only necessary SNS permissions.

### 5. Enable CloudTrail
Monitor SNS API calls for security auditing.

---

## 📊 Monitoring

### CloudWatch Metrics
Monitor these SNS metrics:
- `NumberOfMessagesPublished`
- `NumberOfNotificationsFailed`
- `NumberOfNotificationsDelivered`

### Application Logs
Check console output for:
```
✅ SNS notification sent to topic: message-id
❌ SNS notification failed: error-message
```

---

## 🚀 Advanced Configuration

### Multiple Email Recipients
Add multiple subscriptions to your SNS topic:
1. Go to SNS topic
2. Create subscription for each email
3. All subscribers receive notifications

### Custom Email Templates
Modify `format_transaction_email()` in `app.py` to customize email content.

### SMS Notifications
Change subscription protocol from "Email" to "SMS" for text messages.

### Webhook Integration
Use "HTTPS" protocol to send notifications to external services (Slack, Discord, etc.).

---

## 📝 Example Configuration

### Complete Setup Example
```bash
# 1. Install dependencies
pip install boto3

# 2. Configure AWS
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name: us-east-1
# Default output format: json

# 3. Set SNS Topic
set SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cryptopulse-notifications

# 4. Run application
python app.py

# 5. Test by making a trade
# Login → Buy/Sell crypto → Check email
```

---

## 🎯 Features Summary

✅ **Automatic email notifications** for all trades
✅ **Professional email formatting** with transaction details
✅ **Mock mode** for development without AWS
✅ **Graceful fallback** if AWS is unavailable
✅ **Detailed logging** for debugging
✅ **Secure credential handling**
✅ **Cost-effective** (free tier covers most usage)
✅ **Easy configuration** via environment variables

---

## 📚 Additional Resources

- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/)
- [Boto3 SNS Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

---

## 🆘 Support

For issues or questions:
1. Check console logs for error messages
2. Verify AWS credentials and permissions
3. Test SNS topic manually in AWS Console
4. Review CloudWatch logs
5. Check this documentation

---

*Last Updated: February 2026*
*Version: 1.0 - AWS SNS Integration*