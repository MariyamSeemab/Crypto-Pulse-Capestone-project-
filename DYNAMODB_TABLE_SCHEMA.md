# DynamoDB Table Schema - CryptoPulse

## 📊 Overview

This document describes all DynamoDB tables used in the CryptoPulse application, including their partition keys, sort keys, and attributes.

---

## 🗄️ Table Summary

| Table Name | Partition Key | Sort Key | Purpose |
|------------|--------------|----------|---------|
| **CryptoPulse_Users** | `username` (String) | None | User accounts and authentication |
| **CryptoPulse_Portfolios** | `username` (String) | None | User cryptocurrency holdings |
| **CryptoPulse_Transactions** | `username` (String) | `timestamp` (String) | Transaction history |
| **CryptoPulse_PriceAlerts** | `username` (String) | `alert_id` (String) | Price alert configurations |

---

## 1️⃣ CryptoPulse_Users Table

### Primary Key
- **Partition Key**: `username` (String)
- **Sort Key**: None

### Attributes
```json
{
  "username": "String",        // Primary key - unique identifier
  "password": "String",        // Hashed password (Werkzeug)
  "email": "String",          // User email address
  "role": "String",           // user | admin | analyst | moderator
  "created_at": "String"      // ISO timestamp
}
```

### Example Item
```json
{
  "username": "demo",
  "password": "pbkdf2:sha256:...",
  "email": "demo@user.com",
  "role": "user",
  "created_at": "2026-02-10T14:30:00.000Z"
}
```

### Access Patterns
- **Get user by username**: `GetItem` with username
- **List all users**: `Scan` (admin only)
- **Check if user exists**: `GetItem` with username

### Indexes
- None (simple key-value lookup)

---

## 2️⃣ CryptoPulse_Portfolios Table

### Primary Key
- **Partition Key**: `username` (String)
- **Sort Key**: None

### Attributes
```json
{
  "username": "String",        // Primary key - user identifier
  "balance": "Number",         // Cash balance (Decimal)
  "holdings": "Map",          // Cryptocurrency holdings
  "created_at": "String"      // ISO timestamp
}
```

### Holdings Structure
```json
{
  "holdings": {
    "bitcoin": 0.00123456,     // Coin ID: quantity
    "ethereum": 0.5,
    "solana": 10.0
  }
}
```

### Example Item
```json
{
  "username": "demo",
  "balance": 9500.50,
  "holdings": {
    "bitcoin": 0.00123456,
    "ethereum": 0.5,
    "solana": 10.0
  },
  "created_at": "2026-02-10T14:30:00.000Z"
}
```

### Access Patterns
- **Get user portfolio**: `GetItem` with username
- **Update balance**: `UpdateItem` with username
- **Update holdings**: `UpdateItem` with username
- **List all portfolios**: `Scan` (admin only)

### Indexes
- None (one portfolio per user)

---

## 3️⃣ CryptoPulse_Transactions Table

### Primary Key
- **Partition Key**: `username` (String)
- **Sort Key**: `timestamp` (String)

### Attributes
```json
{
  "username": "String",        // Partition key - user identifier
  "timestamp": "String",       // Sort key - ISO timestamp
  "transaction_id": "String",  // UUID for transaction
  "type": "String",           // buy | sell
  "coin_id": "String",        // Cryptocurrency identifier
  "quantity": "Number",       // Amount of crypto (Decimal)
  "price": "Number",          // Price per unit (Decimal)
  "amount": "Number"          // Total transaction amount (Decimal)
}
```

### Example Item
```json
{
  "username": "demo",
  "timestamp": "2026-02-10T14:30:45.123Z",
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "buy",
  "coin_id": "bitcoin",
  "quantity": 0.00123456,
  "price": 45000.00,
  "amount": 55.56
}
```

### Access Patterns
- **Get user transactions**: `Query` with username
- **Get recent transactions**: `Query` with username, limit, descending
- **Get transactions by date range**: `Query` with username and timestamp range
- **Get all transactions**: `Scan` (admin only)

### Indexes
- None (composite key provides efficient queries)

### Query Examples
```python
# Get all transactions for a user
response = table.query(
    KeyConditionExpression=Key('username').eq('demo')
)

# Get recent 10 transactions
response = table.query(
    KeyConditionExpression=Key('username').eq('demo'),
    ScanIndexForward=False,  # Descending order
    Limit=10
)

# Get transactions in date range
response = table.query(
    KeyConditionExpression=Key('username').eq('demo') & 
                          Key('timestamp').between('2026-02-01', '2026-02-28')
)
```

---

## 4️⃣ CryptoPulse_PriceAlerts Table

### Primary Key
- **Partition Key**: `username` (String)
- **Sort Key**: `alert_id` (String)

### Attributes
```json
{
  "username": "String",        // Partition key - user identifier
  "alert_id": "String",       // Sort key - UUID
  "coin_id": "String",        // Cryptocurrency to monitor
  "target_price": "Number",   // Price threshold (Decimal)
  "condition": "String",      // above | below
  "active": "Boolean",        // Alert enabled/disabled
  "created_at": "String",     // ISO timestamp
  "triggered_at": "String"    // ISO timestamp (optional)
}
```

### Example Item
```json
{
  "username": "demo",
  "alert_id": "550e8400-e29b-41d4-a716-446655440001",
  "coin_id": "bitcoin",
  "target_price": 50000.00,
  "condition": "above",
  "active": true,
  "created_at": "2026-02-10T14:30:00.000Z"
}
```

### Access Patterns
- **Get user alerts**: `Query` with username
- **Get specific alert**: `GetItem` with username and alert_id
- **Update alert**: `UpdateItem` with username and alert_id
- **Delete alert**: `DeleteItem` with username and alert_id
- **Get all active alerts**: `Scan` with filter (for monitoring)

### Indexes
- None (composite key provides efficient queries)

---

## 🔑 Key Design Decisions

### Why These Partition Keys?

#### 1. **username as Partition Key**
- ✅ **Natural identifier**: Users are the primary entity
- ✅ **Even distribution**: Users are evenly distributed
- ✅ **Access patterns**: Most queries are user-specific
- ✅ **Scalability**: Each user's data is independent

#### 2. **timestamp as Sort Key (Transactions)**
- ✅ **Chronological ordering**: Natural sort order
- ✅ **Range queries**: Easy to query by date range
- ✅ **Recent items**: Efficient retrieval of latest transactions
- ✅ **No duplicates**: Timestamp + UUID ensures uniqueness

#### 3. **alert_id as Sort Key (Price Alerts)**
- ✅ **Multiple alerts**: Users can have many alerts
- ✅ **Unique identification**: UUID ensures no conflicts
- ✅ **Easy management**: Simple CRUD operations
- ✅ **Scalability**: No limit on alerts per user

---

## 📈 Capacity Planning

### Billing Mode
**PAY_PER_REQUEST** (On-Demand)
- No capacity planning required
- Pay only for what you use
- Automatic scaling
- Ideal for variable workloads

### Estimated Costs (Monthly)

#### Low Usage (100 users, 1,000 transactions)
- **Reads**: ~10,000 reads = $1.25
- **Writes**: ~1,000 writes = $1.25
- **Storage**: <1 GB = $0.25
- **Total**: ~$2.75/month

#### Medium Usage (1,000 users, 10,000 transactions)
- **Reads**: ~100,000 reads = $12.50
- **Writes**: ~10,000 writes = $12.50
- **Storage**: ~5 GB = $1.25
- **Total**: ~$26.25/month

#### High Usage (10,000 users, 100,000 transactions)
- **Reads**: ~1,000,000 reads = $125
- **Writes**: ~100,000 writes = $125
- **Storage**: ~50 GB = $12.50
- **Total**: ~$262.50/month

---

## 🔍 Query Patterns

### Common Queries

#### Get User Profile
```python
response = users_table.get_item(
    Key={'username': 'demo'}
)
```

#### Get User Portfolio
```python
response = portfolios_table.get_item(
    Key={'username': 'demo'}
)
```

#### Get Recent Transactions
```python
response = transactions_table.query(
    KeyConditionExpression=Key('username').eq('demo'),
    ScanIndexForward=False,
    Limit=20
)
```

#### Get Active Alerts
```python
response = price_alerts_table.query(
    KeyConditionExpression=Key('username').eq('demo'),
    FilterExpression=Attr('active').eq(True)
)
```

---

## 🛡️ Security Best Practices

### 1. Encryption
- ✅ **At Rest**: Enabled by default
- ✅ **In Transit**: HTTPS/TLS
- ✅ **KMS**: Optional customer-managed keys

### 2. Access Control
- ✅ **IAM Policies**: Least privilege access
- ✅ **VPC Endpoints**: Private network access
- ✅ **Audit Logging**: CloudTrail enabled

### 3. Data Protection
- ✅ **Point-in-Time Recovery**: Enabled
- ✅ **Backups**: Automatic daily backups
- ✅ **Versioning**: Track data changes

---

## 📊 Monitoring

### CloudWatch Metrics
- `UserErrors`: Track client errors
- `SystemErrors`: Track server errors
- `ConsumedReadCapacityUnits`: Monitor reads
- `ConsumedWriteCapacityUnits`: Monitor writes
- `ThrottledRequests`: Track throttling

### Alarms to Set
- High error rate (>1%)
- Throttled requests (>0)
- High latency (>100ms)
- Storage approaching limits

---

## 🔄 Migration Guide

### From Local to DynamoDB

#### Step 1: Export Local Data
```python
import json

# Export users
with open('users_export.json', 'w') as f:
    json.dump(users_db, f)

# Export portfolios
with open('portfolios_export.json', 'w') as f:
    json.dump(user_portfolios, f)
```

#### Step 2: Import to DynamoDB
```python
import boto3
import json

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('CryptoPulse_Users')

# Import users
with open('users_export.json', 'r') as f:
    users = json.load(f)
    for username, data in users.items():
        users_table.put_item(Item={
            'username': username,
            **data
        })
```

---

## 📝 Quick Reference

### Table Names
```
CryptoPulse_Users
CryptoPulse_Portfolios
CryptoPulse_Transactions
CryptoPulse_PriceAlerts
```

### Partition Keys
```
Users:        username
Portfolios:   username
Transactions: username
PriceAlerts:  username
```

### Sort Keys
```
Users:        None
Portfolios:   None
Transactions: timestamp
PriceAlerts:  alert_id
```

### Common Operations
```python
# Get Item
table.get_item(Key={'username': 'demo'})

# Put Item
table.put_item(Item={...})

# Update Item
table.update_item(
    Key={'username': 'demo'},
    UpdateExpression='SET balance = :val',
    ExpressionAttributeValues={':val': 10000}
)

# Query
table.query(
    KeyConditionExpression=Key('username').eq('demo')
)

# Scan (use sparingly)
table.scan()
```

---

## 🎯 Summary

All CryptoPulse DynamoDB tables use **`username`** as the partition key because:

1. ✅ **User-centric design**: All data belongs to users
2. ✅ **Efficient queries**: Most operations are user-specific
3. ✅ **Even distribution**: Users are naturally distributed
4. ✅ **Scalability**: Each user's data is independent
5. ✅ **Simple access patterns**: Easy to understand and maintain

**Sort keys** are used where multiple items per user are needed:
- **Transactions**: Sorted by `timestamp` for chronological order
- **Price Alerts**: Sorted by `alert_id` for unique identification

---

*Last Updated: February 2026*
*Version: 1.0 - DynamoDB Schema Documentation*